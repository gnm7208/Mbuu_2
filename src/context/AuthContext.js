import { createContext, useEffect, useState } from "react";
export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const json = localStorage.getItem("mbuu_user");
    return json ? JSON.parse(json) : null;
  });
  const [token, setToken] = useState(localStorage.getItem("mbuu_token") || null);

  useEffect(() => {
    user ? localStorage.setItem("mbuu_user", JSON.stringify(user)) : localStorage.removeItem("mbuu_user");
  }, [user]);
  useEffect(() => {
    token ? localStorage.setItem("mbuu_token", token) : localStorage.removeItem("mbuu_token");
  }, [token]);

  const logout = () => { setUser(null); setToken(null); };

  return <AuthContext.Provider value={{ user, token, setUser, setToken, logout }}>{children}</AuthContext.Provider>;
}
