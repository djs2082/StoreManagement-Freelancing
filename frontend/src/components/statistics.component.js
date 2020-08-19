import React, { Component } from 'react'
import Chart from "react-google-charts";
import Menu from './menu.component';
import axios from 'axios';

class Graph extends Component {
	constructor(props) {
		super(props)

		if (sessionStorage.getItem('token') === 'undefined' || sessionStorage.getItem('username') === 'undefined') {
			this.props.history.push('/')
		}
		this.state = {
			data: ['Sale', ''],
			errors: []
		}
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
	componentDidMount = () => {
		var headers = {
			'Authorization': 'Token ' + sessionStorage.getItem('token')
		}
		axios.get(window.API_URL+'/receipts/sales_for_graph/', {
			headers: headers
		})
			.then(response => {
				if (response.status == 200) {

					if (response.data.status == 404) {
						this.errorOccured(404, response.data.error.error, "Error")
					}

					else if (response.data.status == 200) {
						var data = []
						if (response.data.status != 404) {
							data.push(this.state.data)

							response.data.Data.date_wise_payment_list.map(sell => {
								let temp = []
								temp.push(sell.date)
								temp.push(sell.amount)
								data.push(temp)


							})
						}
						this.setState({ graph_data: data })

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
			return (<div data-key={error.id} className='alert alert-danger alert-dismissible override'>
				<a href="#" onClick={this.deleteError} class="close" data-dismiss="alert" aria-label="close">&times;</a>
				<div><strong>error!</strong> {error.error}</div>
				<div><strong>message</strong> {error.message}</div>
				<div><strong>status</strong> {error.status}</div></div>)
		}) : ("")
		return (
			<div>
				{Error}
				<Menu></Menu>
				<div style={{ display: 'flex', maxWidth: 900 }}>
					<Chart
						width={1400}
						height={1300}
						chartType="ColumnChart"
						loader={<h1 style={{ color: "black" }}>...Loading Chart</h1>}
						data={this.state.graph_data}
						options={{
							title: 'Sales of This Month',
							chartArea: { maxWidth: '75%', maHeight: '75%', backgroundColor: "black" },
							hAxis: {
								title: 'Date',
							},
							vAxis: {
								title: 'Sale',
							},
						}}
						legendToggle
					/>

				</div></div>)
	}
}
export default Graph;