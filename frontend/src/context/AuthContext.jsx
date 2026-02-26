import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  // ✅ Restore auth from BOTH storages
  useEffect(() => {
    const storedUser =
      localStorage.getItem("lexi_user") ||
      sessionStorage.getItem("lexi_user");

    const storedToken =
      localStorage.getItem("lexi_token") ||
      sessionStorage.getItem("lexi_token");

    if (storedUser && storedToken) {
      setUser(JSON.parse(storedUser));
      setToken(storedToken);
    }
  }, []);

  // ✅ Login
  const login = (userData, authToken, remember) => {
    setUser(userData);
    setToken(authToken);

    if (remember) {
      localStorage.setItem("lexi_user", JSON.stringify(userData));
      localStorage.setItem("lexi_token", authToken);
    } else {
      sessionStorage.setItem("lexi_user", JSON.stringify(userData));
      sessionStorage.setItem("lexi_token", authToken);
    }
  };

  // ✅ Logout
  const logout = () => {
    setUser(null);
    setToken(null);

    localStorage.removeItem("lexi_user");
    localStorage.removeItem("lexi_token");
    sessionStorage.removeItem("lexi_user");
    sessionStorage.removeItem("lexi_token");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);