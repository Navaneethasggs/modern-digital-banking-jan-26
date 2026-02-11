import React, { createContext, useState, useEffect, useCallback } from "react";
import { loginAPI, registerAPI, fetchCurrentUser } from "../features/auth/AuthAPI";
import { getToken, setToken, removeToken } from "../features/auth/AuthService";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const isAuthenticated = !!user;

    // On mount, check if a token exists and fetch the user
    useEffect(() => {
        const token = getToken();
        if (token) {
            fetchCurrentUser()
                .then((res) => setUser(res.data))
                .catch(() => {
                    removeToken();
                    setUser(null);
                })
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    const login = useCallback(async (email, password) => {
        const { data } = await loginAPI(email, password);
        setToken(data.access_token);
        const userRes = await fetchCurrentUser();
        setUser(userRes.data);
        return userRes.data;
    }, []);

    const register = useCallback(async ({ name, email, password, phone }) => {
        const { data } = await registerAPI({ name, email, password, phone });
        setToken(data.access_token);
        const userRes = await fetchCurrentUser();
        setUser(userRes.data);
        return userRes.data;
    }, []);

    const logout = useCallback(() => {
        removeToken();
        setUser(null);
    }, []);

    return (
        <AuthContext.Provider
            value={{ user, loading, isAuthenticated, login, register, logout }}
        >
            {children}
        </AuthContext.Provider>
    );
}
