import React, { Component } from 'react';
import md5 from 'md5-hash';
import '../css/login.css';
import axios from 'axios';

class Login extends Component {
	constructor(props) {
		super(props)
		sessionStorage.clear()
		this.state = {
			username: null,
			password: null,
			isLoggedIn: false,
			errors: [],
		}
	}

	handleChange = (e) => {
		this.setState({
			[e.target.name]: e.target.value
		})
	}

	errorOccured = (status, err, message) => {
		let error = { "id": this.state.errors.length + 1, "status": status, "error": err, "message": message }
		let errors = this.state.errors
		errors.push(error)

		this.setState(errors)
	}

	deleteError = (e) => {
		let key = e.currentTarget.parentNode.getAttribute("data-key");

		let errors = this.state.errors.filter(error => {
			return parseInt(error.id) !== parseInt(key);
		})
		this.setState({ errors: errors })
	}




	handleSubmit = (e) => {
		e.preventDefault();
		axios.post(window.API_URL+"/owner/login_user/", { 'username': this.state.username, 'password': this.state.password })
			.then(response => {
				console.log(response)
				if (response.status == 200) {


					if (response.data.status == 404) {


						this.errorOccured(404, response.data.error.error, "Invalid Username or Password")
					}
					else if (response.data.status == 200) {


						this.setState({ isLoggedIn: true, error: false })
						sessionStorage.setItem('username', this.state.username);
						sessionStorage.setItem('token', response.data.Data.token);
						this.props.history.push('/home');
					}
					else {

						this.errorOccured(response.data.status, response.error.error, "Unknown Error Occurred")
					}
				}
				else {

					this.errorOccured(500, "erro occurred", "Unknown error occurred")

				}
			})
			.catch(error => {

				this.errorOccured(500, "error occurred", error.message)
			});

	}

	render() {
		var Error = this.state.errors.length ? this.state.errors.map(error => {
			return (<div data-key={error.id} className='alert alert-danger alert-dismissible'>
				<a href="#" onClick={this.deleteError} class="close" data-dismiss="alert" aria-label="close">&times;</a>
				<div><strong>error!</strong> {error.error}</div>
				<div><strong>message</strong> {error.message}</div>
				<div><strong>status</strong> {error.status}</div></div>)
		}) : ("")



		return (
			<div className="container">
				{Error}
				<div className="d-flex justify-content-center h-100">
					<div className="card">
						<div className="card-header">
							<h3>{window.SIGN_IN_MESSAGE}</h3>
						</div>
						<div className="card-body">
							<form onSubmit={this.handleSubmit} id="login_form">
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i className="fas fa-user"></i></span>
									</div>
									<input onChange={this.handleChange} type="text" className="form-control" id="username" name="username" placeholder="username" required></input>

								</div>
								<div className="input-group form-group">
									<div className="input-group-prepend">
										<span className="input-group-text"><i className="fas fa-key"></i></span>
									</div>
									<input onChange={this.handleChange} type="password" className="form-control" id="password" name="password" placeholder="password" required></input>
								</div>
								<div className="form-group">
									<input type="submit" value="Login" className="btn-lg float-right login_btn" />
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>
		)
	}
}
export default Login;