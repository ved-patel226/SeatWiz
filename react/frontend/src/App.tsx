import { GoogleOAuthProvider } from "@react-oauth/google";
import Auth from "./auth/auth";
import getAPI from "./functions/getAPI";
import React from "react";
import { get } from "http";
import fetchAPI from "./functions/getAPI";

function App() {
  console.log(fetchAPI({ url: "is_authenticated" }));

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

export default App;
