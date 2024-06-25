import App from "@/app/App";
import { lazy } from "react";
import { createBrowserRouter } from "react-router-dom";

const LoginPage = lazy(() => import("@/pages/LoginPage/LoginPage"));

const router = createBrowserRouter([
  {
    id: "root",
    // todo - /로 바꾸고 login auth 체크 로직 추가
    path: "/",
    element: <App />,
    children: [
      //   {
      //     index: true,
      //     element: <PublicPage />,
      //   },
      {
        index: true,
        path: "login",
        element: <LoginPage />,
      },
      //   {
      //     path: "protected",
      //     element: <ProtectedPage />,
      //   },
    ],
  },
  //   {
  //     path: "/logout",
  //     async action() {
  //       // We signout in a "resource route" that we can hit from a fetcher.Form
  //       await fakeAuthProvider.signout();
  //       return redirect("/");
  //     },
  //   },
]);

export default router;
