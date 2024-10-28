import { GoogleOAuthProvider } from "@react-oauth/google";
import Auth from "./auth/auth";
import getAPI from "./functions/getAPI";
import React, { useEffect } from "react";
import { get } from "http";
import fetchAPI from "./functions/getAPI";
import Cookies from "cookiejs";

function App() {
  const [auth, setAuth] = React.useState(false);

  const checkAuth = async () => {
    const user = Cookies.get("user");
    console.log("User:", user);
    if (user) {
      setAuth(true);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  if (auth === false) {
    return (
      <div className="App">
        <header className="App-header">
          <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
            <Auth />
          </GoogleOAuthProvider>
        </header>
      </div>
    );
  }

  return <h1>Logged in</h1>;
}

export default App;
