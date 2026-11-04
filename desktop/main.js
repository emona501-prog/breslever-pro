// ברסלב PRO למחשב (Windows) – אותה אפליקציה בדיוק, עובדת גם בלי אינטרנט, ומתעדכנת לבד מעמוד ההורדות
const { app, BrowserWindow, protocol, shell, net, Menu } = require('electron');
const path = require('path');
const { pathToFileURL } = require('url');

protocol.registerSchemesAsPrivileged([{ scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true, allowServiceWorkers: true, corsEnabled: true, stream: true } }]);
const ROOT = path.join(__dirname, 'app');
let win = null;

if (!app.requestSingleInstanceLock()) app.quit();
app.on('second-instance', () => { if (win) { if (win.isMinimized()) win.restore(); win.focus(); } });

function createWindow() {
  win = new BrowserWindow({
    width: 1200, height: 880, minWidth: 380, minHeight: 500, backgroundColor: '#020E29', autoHideMenuBar: true,
    title: 'ברסלב PRO', icon: path.join(__dirname, 'icon.png'),
    webPreferences: { contextIsolation: true, spellcheck: false }
  });
  const ext = url => !url.startsWith('app://');
  win.webContents.setWindowOpenHandler(({ url }) => { if (ext(url)) { shell.openExternal(url); return { action: 'deny' }; } return { action: 'allow' }; });
  win.webContents.on('will-navigate', (e, url) => { if (ext(url)) { e.preventDefault(); shell.openExternal(url); } });
  win.loadURL('app://local/index.html');
}

app.whenReady().then(() => {
  protocol.handle('app', req => {
    let p = decodeURIComponent(new URL(req.url).pathname || '/');
    if (p === '/' || p === '') p = '/index.html';
    const f = path.normalize(path.join(ROOT, p));
    if (!f.startsWith(ROOT)) return new Response('forbidden', { status: 403 });
    return net.fetch(pathToFileURL(f).toString());
  });
  Menu.setApplicationMenu(null);
  app.setAppUserModelId('com.chaiproductions.breslovpro');
  createWindow();
  try { const { autoUpdater } = require('electron-updater'); autoUpdater.checkForUpdatesAndNotify().catch(() => {}); } catch (e) {}
});
app.on('window-all-closed', () => app.quit());
