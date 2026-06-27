import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API_URL from "../config";

function SignupPage() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("");
    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        const finalName = name.trim();

        const res = await fetch(`${API_URL}/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: finalName, email, password: pass }),
        });

        if (!res.ok) {
			const err = await res.json().catch(() => ({}));
			alert(err.error || "Signup failed");
			return;
        }

        const data = await res.json();
        navigate(`/user/${data.user_id}`, { state: { user_id: data.user_id, name: data.name, email: data.email } });
    }

    return (
        <div>
            <h1>Sign up</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Name:{" "}
                    <input
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Your name"
                    />
                </label>
                <label>
                    Email:{" "}
                    <input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Your Email ID"
                    />
                </label>
                <label>
                    Password:{" "}
                    <input
                        type="password"
                        value={pass}
                        onChange={(e) => setPass(e.target.value)}
                        placeholder="Create Password"
                    />
                </label>
                <button type="submit">Create account</button>
            </form>
            <p>
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    );
}

export default SignupPage;