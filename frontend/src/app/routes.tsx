import { createBrowserRouter } from 'react-router';
import Root from './components/Root';
import { MultiStepForm } from './components/MultiStepForm';
import { StreamingPanel } from './components/StreamingPanel';
import { ResultsDashboard } from './components/ResultsDashboard';

export const router = createBrowserRouter([
  {
    path: '/',
    Component: Root,
    children: [
      { index: true, Component: MultiStepForm },
      { path: 'streaming', Component: StreamingPanel },
      { path: 'results', Component: ResultsDashboard },
    ],
  },
]);
