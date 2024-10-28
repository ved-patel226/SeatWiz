import React, { useState } from "react";
import GoogleIcon from "@mui/icons-material/Google";
import IconButton from "@mui/material/IconButton";
import { useGoogleLogin } from "@react-oauth/google";
import UserAvatar from "./userAvatar";
import App from "../App";
import Cookies from "cookiejs"; // Import cookie management library

interface CodeResponse {
  code: string;
}

interface User {
  name: string;
}

async function getUserInfo(
  codeResponse: CodeResponse
): Promise<{ user: User }> {
  const response = await fetch("http://127.0.0.1:5000/google_login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code: codeResponse.code }),
  });
  return await response.json();
}

async function getProtected(): Promise<void> {
  await fetch("http://127.0.0.1:5000/protected", {
    method: "GET",
    credentials: "include",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((msg) => console.log(msg));
}

export default function Auth() {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);

  const googleLogin = useGoogleLogin({
    flow: "auth-code",
    onSuccess: async (codeResponse: CodeResponse) => {
      const loginDetails = await getUserInfo(codeResponse);
      setLoggedIn(true);
      setUser(loginDetails.user);

      // Set user information in cookies
      Cookies.set("user", JSON.stringify(loginDetails.user), { expires: 1 }); // expires in 1 day
    },
  });

  const handleLogout = () => {
    getProtected(); // Optionally call a function to log out or invalidate the session on the server
    setLoggedIn(false);
    setUser(null);

    // Remove user information from cookies
    Cookies.remove("user");
  };

  return (
    <>
      {!loggedIn ? (
        <IconButton
          color="primary"
          aria-label="holup"
          onClick={() => googleLogin()}
        >
          <GoogleIcon fontSize="large" />
        </IconButton>
      ) : (
        <App />
      )}
    </>
  );
}
