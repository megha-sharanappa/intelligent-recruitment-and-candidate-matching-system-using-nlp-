import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;
const FLASK_PORT = 5000;
const FLASK_URL = `http://127.0.0.1:${FLASK_PORT}`;

// Ensure Python Flask process is running
let pythonProcess: any = null;

function startFlask() {
  console.log('Ensuring Python Flask recruitment backend is running on port 5000...');
  pythonProcess = spawn('python3', ['app.py'], {
    cwd: path.resolve(__dirname, '.'),
    stdio: 'inherit',
    env: { ...process.env, FLASK_PORT: String(FLASK_PORT), PYTHONUNBUFFERED: '1' }
  });

  pythonProcess.on('error', (err: any) => {
    console.error('Failed to start Python process:', err);
  });

  pythonProcess.on('exit', (code: number, signal: string) => {
    console.log(`Python process exited with code ${code} and signal ${signal}`);
  });
}

startFlask();

// Proxy all requests to Flask app with full iFrame & HTTPS cookie support
app.use(
  '/',
  createProxyMiddleware({
    target: FLASK_URL,
    changeOrigin: true,
    ws: true,
    on: {
      proxyReq: (proxyReq: any, req: any) => {
        // Forward HTTPS proto so Flask knows it is running behind an HTTPS load balancer
        proxyReq.setHeader('x-forwarded-proto', 'https');
      },
      proxyRes: (proxyRes: any, req: any, res: any) => {
        const sc = proxyRes.headers['set-cookie'];
        if (sc && Array.isArray(sc)) {
          proxyRes.headers['set-cookie'] = sc.map((cookieStr: string) => {
            let updated = cookieStr;
            // Ensure SameSite=None for iframe support
            if (!/samesite=/i.test(updated)) {
              updated += '; SameSite=None';
            } else {
              updated = updated.replace(/samesite=\w+/i, 'SameSite=None');
            }
            // Ensure Secure for iframe support
            if (!/secure/i.test(updated)) {
              updated += '; Secure';
            }
            // Ensure Partitioned for modern Chrome third-party cookie support
            if (!/partitioned/i.test(updated)) {
              updated += '; Partitioned';
            }
            // For cookie deletion, ensure HttpOnly and Path=/ match original cookie
            if (/Max-Age=0|Expires=Thu, 01 Jan 1970/i.test(updated)) {
              if (!/httponly/i.test(updated)) {
                updated += '; HttpOnly';
              }
              if (!/path=/i.test(updated)) {
                updated += '; Path=/';
              }
            }
            return updated;
          });
        }
      },
      error: (err: any, req: any, res: any) => {
        console.error('Proxy connection notice:', err.message);
        if (res && res.status) {
          res.status(502).send(`
            <html>
              <head><meta http-equiv="refresh" content="2"></head>
              <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h2>Starting Recruitment System...</h2>
                <p>The Python Flask application is initializing. Please wait a moment.</p>
              </body>
            </html>
          `);
        }
      }
    }
  })
);

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Express proxy server running at http://0.0.0.0:${PORT} forwarding to Flask at ${FLASK_URL}`);
});

process.on('SIGTERM', () => {
  if (pythonProcess) pythonProcess.kill();
  process.exit(0);
});

process.on('SIGINT', () => {
  if (pythonProcess) pythonProcess.kill();
  process.exit(0);
});
