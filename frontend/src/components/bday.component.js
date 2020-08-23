import React, { Component } from 'react'
import { MDBDataTableV5 } from 'mdbreact';
import Menu from './menu.component'
import axios from 'axios';

class Birthday extends Component {
  constructor(props) {
    super(props);
    if (sessionStorage.getItem('token') === 'undefined' || sessionStorage.getItem('username') === 'undefined') {
      this.props.history.push('/')
    }
    this.state = {
      datatable: {
        columns: [
          {
            label: 'FirstName',
            field: 'fname',
            width: 150,
          },
          {
            label: 'LastName',
            field: 'lname',
            width: 270,
          },
          {
            label: 'Mobile',
            field: 'mobile',
            width: 200,
          },
          {
            label: 'Date',
            field: 'date',
            width: 150,
          },
          {
            label: 'DOB',
            field: 'birth_day',
            width: 150,
          }
        ],
        rows: [],
      },
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

  update_rows = (response) => {
    try {
    console.log(response)
      let columns = this.state.datatable.columns
      let rows = this.state.datatable.rows
      response.Data.forEach(element => { rows.push(element) })
      let datatable = { columns: columns, rows: rows }
      this.setState({ datatable: datatable })
    }
    catch (error) {
      this.errorOccured(400, "error occurred", error.toString())

    }
  }
  get_next = (response) => {


    const headers = {
      'Authorization': 'Token ' + sessionStorage.getItem('token')
    }

    axios.get(response, { headers: headers })
      .then(result => {
        if (result.status == 200) {

          if (result.data.status == 404) {
            this.errorOccured(404, result.data.error.error, "Error")
          }

          else if (result.data.status == 200) {
            this.update_rows(result.data);
          }
          else {
            this.errorOccured(result.data.status, result.error.error, "Unknown Error Occurred")
          }
        }
        else {
          this.errorOccured(500, "erro occurred", "Unknown error occurred")

        }
      })
      .catch(error => {
      });


  }

  componentDidMount = () => {
    const headers = {
      'Authorization': 'Token ' + sessionStorage.getItem('token')
    }
    axios.get(window.API_URL+'/customers/bday/', {
      headers: headers
    })
      .then(response => {

        if (response.status == 200) {

          if (response.data.status == 404) {
            this.errorOccured(404, response.data.error.error, "Error")
          }

          else if (response.data.status == 200) {
            this.update_rows(response.data);
            this.get_next(response.data.Data.links.next)

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

        // this.errorOccured(500, "error occurred", error.toString())
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
        <Menu />
        {Error}
        <div style={{ backgroundColor: "black", fontSize: "15px", color: "green" }}>
          <MDBDataTableV5 className="table-responsive" style={{ textAlign: "left", backgroundColor: "black", fontSize: "20px", color: "white" }} hover entriesOptions={[10, 20, 25]} entries={10} pagesAmount={4} data={this.state.datatable} searchTop searchBottom={false} />
        </div>
      </div>

    )

  }
}
export default Birthday;