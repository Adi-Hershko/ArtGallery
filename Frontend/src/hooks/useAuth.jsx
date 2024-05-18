import { useUser } from '../contexts/UserContext';

export function useAuth() {
    const { user, setUser } = useUser();

    const login = (userData) => {
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('user');
    };

    return { user, login, logout };
}