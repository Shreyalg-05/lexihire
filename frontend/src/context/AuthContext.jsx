import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  /* Check login when app loads */

  useEffect(() => {

    const storedAuth = localStorage.getItem("lexihire_auth");

    if (storedAuth === "true") {
      setIsAuthenticated(true);
    }

  }, []);

  /* Login */

  const login = () => {

    localStorage.setItem("lexihire_auth", "true");

    setIsAuthenticated(true);

  };

  /* Logout */

  const logout = () => {

    localStorage.removeItem("lexihire_auth");

    setIsAuthenticated(false);

  };

  return (

    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>

      {children}

    </AuthContext.Provider>

  );

};

export const useAuth = () => useContext(AuthContext);