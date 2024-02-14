import React, { createContext } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import GeneralStore from './stores/GeneralStore';

const root = ReactDOM.createRoot(document.getElementById('root'));

export const Context = createContext({
  general: new GeneralStore(),
});

root.render(
  <React.StrictMode>
    <Context.Provider
      value={{ general: new GeneralStore(), }}
    >
      <App />
    </Context.Provider>
  </React.StrictMode>
);