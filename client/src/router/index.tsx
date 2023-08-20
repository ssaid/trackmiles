import { createBrowserRouter } from "react-router-dom";
import { App } from "../App";
import { AboutView } from "../views/AboutView";
import { AnalyticsView } from "../views/AnalyticsView";
import { ErrorView } from "../views/ErrorView";
import { HomeView } from "../views/HomeView";


export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { path: "/", element: <HomeView /> },
      {
        path: 'analytics',
        element: <AnalyticsView />,
      },
      {
        path: 'about',
        element: <AboutView />,
      },
    ],
    errorElement: <ErrorView />,
  },
]);
