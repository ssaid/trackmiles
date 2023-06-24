import { createBrowserRouter } from "react-router-dom";
import { App } from "../App";
import { AnalyticsView } from "../views/AnalyticsView";
import { Home } from "../views/Home";


export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { path: "/", element: <Home /> },
    ]
  },
  {
    path: 'analytics',
    element: <AnalyticsView />,
  }
]);
