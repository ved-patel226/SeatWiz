import React, { useEffect, useState } from "react";
import GoogleIcon from "@mui/icons-material/Google";
import IconButton from "@mui/material/IconButton";
import { useGoogleLogin } from "@react-oauth/google";
import Cookies from "cookiejs";

interface CodeResponse {
  code: string;
}

interface User {
  name: string;
  email: string;
  email_verified: boolean;
  family_name: string;
  given_name: string;
  picture: string;
  sub: string;
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
  });
}

export default function Auth() {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const userCookie = Cookies.get("user");
    console.log("Checking for user cookie on reload:", userCookie);
    if (userCookie) {
      try {
        const parsedUser: User = JSON.parse(userCookie);
        setUser(parsedUser);
        setLoggedIn(true);
      } catch (error) {
        console.error("Failed to parse user cookie:", error);
      }
    }
  }, []);

  const googleLogin = useGoogleLogin({
    flow: "auth-code",
    onSuccess: async (codeResponse: CodeResponse) => {
      console.log("Attempting to log in...");
      const loginDetails = await getUserInfo(codeResponse);
      console.log("Received login details:", loginDetails);

      if (loginDetails && loginDetails.user) {
        setLoggedIn(true);
        setUser(loginDetails.user);
        Cookies.set("user", JSON.stringify(loginDetails.user), { expires: 1 });
        console.log("User set in state:", loginDetails.user);
      } else {
        console.error("Login details not valid");
      }
    },
  });

  const handleLogout = () => {
    getProtected();
    setLoggedIn(false);
    setUser(null);
    Cookies.remove("user");
    console.log("User cookie removed");
  };

  return (
    <>
      {!loggedIn ? (
        <IconButton
          sx={{
            backgroundColor: "none",
            color: "#a6adbb",
            "&:hover": {
              backgroundColor: "#383f47",
              color: "#a6adbb",
            },
          }}
          className="w-12 h-12"
          aria-label="holup"
          onClick={() => googleLogin()}
        >
          <GoogleIcon fontSize="medium" className="" />
        </IconButton>
      ) : (
        <button className="btn btn-ghost btn-circle" onClick={handleLogout}>
          <img
            className="w-7 rounded-3xl cursor-pointer"
            src={user?.picture}
            alt=""
          />
        </button>
      )}
    </>
  );
}
