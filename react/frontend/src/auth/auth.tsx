import React, { useState } from "react";
import GoogleIcon from "@mui/icons-material/Google";
import IconButton from "@mui/material/IconButton";
import { useGoogleLogin } from "@react-oauth/google";
import UserAvatar from "./userAvatar";

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
      // console.log(loginDetails);
      setUser(loginDetails.user);
    },
  });

  const handleLogout = () => {
    getProtected();
    setLoggedIn(false);
    setUser(null);
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
        <UserAvatar userName={user?.name} onClick={handleLogout} />
      )}
    </>
  );
}
