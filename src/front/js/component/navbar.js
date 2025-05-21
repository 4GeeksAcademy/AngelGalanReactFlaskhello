import React from "react";
import { Link,useNavigate } from "react-router-dom";

export const Navbar = () => {
	const navigate = useNavigate();
	const isLoggedIn = !!sessionStorage.getItem("token");

	const handleLogout = () => {
		sessionStorage.removeItem("token");
		navigate("/login");
	};
	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto">
					<Link to="/demo">
						<button className="btn btn-primary">Check the Context in action</button>
					</Link>
					{isLoggedIn && (
						<button className="btn btn-danger" onClick={handleLogout}>
							cerrar sesion
						</button>
					)}
				</div>
			</div>
		</nav>
	);
};
