import React from 'react';
import { createRoot } from 'react-dom/client';
import { Excalidraw, convertToExcalidrawElements, exportToSvg, restoreElements } from '@excalidraw/excalidraw';

window.diagramTools = { convertToExcalidrawElements, exportToSvg, restoreElements };
window.mountEditor = (scene) => new Promise((resolve) => {
  createRoot(document.getElementById('editor')).render(React.createElement(Excalidraw, {
    initialData: scene,
    excalidrawAPI: (api) => { window.editorAPI = api; resolve(true); },
  }));
});
