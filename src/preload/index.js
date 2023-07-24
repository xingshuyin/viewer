import { contextBridge, ipcRenderer } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'
import fs from 'fs'
// Custom APIs for renderer
const api = {}

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
if (process.contextIsolated) {
  try {
    console.log('try')
    contextBridge.exposeInMainWorld('electron', electronAPI)
    contextBridge.exposeInMainWorld('api', api)
    contextBridge.exposeInMainWorld('ipcRenderer', ipcRenderer)
    contextBridge.exposeInMainWorld('fs', fs)
  } catch (error) {
    console.log('error')
    console.error(error)
  }
} else {
  console.log('else')
  window.electron = electronAPI
  window.api = api
  window.ipcRenderer = ipcRenderer
  window.fs = fs
}
