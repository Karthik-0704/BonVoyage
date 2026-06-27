import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API_URL from "../config";

function LoginPage() {
    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("");
    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        const finalEmail = email.trim();

        const res = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: finalEmail, password: pass }),
        });

        if (!res.ok) {
			const err = await res.json().catch(() => ({}));
			alert(err.error || "Login failed");
			return;
        }

        const data = await res.json();
        navigate(`/user/${data.user_id}`, { state: { user_id: data.user_id, name: data.name, email: data.email } });
    }

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Email:{" "}
                    <input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter Email ID"
                    />
                </label>
                <label>
                    Password:{" "}
                    <input
                        type="password"
                        value={pass}
                        onChange={(e) => setPass(e.target.value)}
                        placeholder="Enter Password"
                    />
                </label>
                <button type="submit">Login</button>
            </form>
            <p>
                Don&apos;t have an account? <Link to="/signup">Sign up</Link>
            </p>
        </div>
    );
}

export default LoginPage;