import { createRoot } from 'react-dom/client';
import { DeveloperFeedback } from './developer-feedback';
import { ProductApp } from './product-app';
import './style.css';

const isDeveloperFeedback = window.location.pathname.replace(/\/$/, '') === '/developer/feedback';

createRoot(document.getElementById('root')!).render(
  isDeveloperFeedback ? <DeveloperFeedback /> : <ProductApp />,
);
