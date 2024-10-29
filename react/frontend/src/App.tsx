import { GoogleOAuthProvider } from "@react-oauth/google";
import Auth from "./auth/auth";
import getAPI from "./functions/getAPI";
import React, { useEffect } from "react";
import { get } from "http";
import fetchAPI from "./functions/getAPI";
import Cookies from "cookiejs";
import NavBar from "./components/navBar";

function App() {
  const [auth, setAuth] = React.useState(false);

  const checkAuth = async () => {
    const user = Cookies.get("user");
    if (user) {
      setAuth(true);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <div className="App">
      <NavBar>
        <header className="App-header inline-flex w-fit h-fit">
          <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
            <Auth />
          </GoogleOAuthProvider>
        </header>
      </NavBar>
    </div>
  );
}

export default App;
