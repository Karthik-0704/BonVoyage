import { Link } from "react-router-dom";

function WelcomePage() {
  return (
    <div>
      <h1>AI Travel Planner</h1>
      <p>Plan your next trip with AI assistance.</p>
      <div>
        <Link to="/login">
          <button>Login</button>
        </Link>
        <Link to="/signup">
          <button>Sign up</button>
        </Link>
      </div>
    </div>
  );
}

export default WelcomePage;