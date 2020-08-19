import React, { Component } from 'react'
import { MDBDataTableV5 } from 'mdbreact';
import Menu from './menu.component'
import '../css/sale.css';
import axios from 'axios';


class Customer extends Component {
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
            width: 270,
          },
          {
            label: 'Amount Paid',
            field: 'amount_payable',
            width: 200,
          },
          {
            label: 'Discount Provided',
            field: 'total_discount',
            sort: 'disabled',
            width: 150,
          },
          {
            label: 'Payment Type',
            field: 'payment_method',
            width: 270,
          },
          {
            label: 'Date',
            field: 'date',
            width: 270,
          },
          {
            label: 'Reciept',
            field: 'receipt_pdf',
            width: 270,
          }
        ],
        rows: [
        ],
      },
      errors: []
    }
    this.payments = "";
    var headers = {
      'Authorization': 'Token ' + sessionStorage.getItem('token')
    }
    axios.get(window.API_URL+'/payments/payments_today/', {
      headers: headers
    })
      .then(response => {

        if (response.status == 200) {

          if (response.data.status == 404) {
            this.errorOccured(404, response.data.error.error, "Error")
          }

          if (response.data.status == 200) {
            var payments = response.data.Data.amount_wise_payment_list.map(payment => {
              return (<tr> <th style={{ color: "green" }}>{payment.name?(payment.name):("deleted payment option")}</th><td>{payment.amount}</td></tr>)
            })
            var total_amount = response.data.Data.total_amount_paid_today
            this.setState({ payments: payments, total_amount: total_amount })

          }
          else {

            this.errorOccured(response.data.status, response.error.error, "Unknown Error Occurred")
          }
        }
        else {

          this.errorOccured(500, "error occurred", "Unknown error occurred")

        }
      })
      .catch(error => {
        // this.errorOccured(500, "error occurred", error.message)
      });
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
      let columns = this.state.datatable.columns
      let rows = this.state.datatable.rows
      if (response.status === 200) {

        response.Data.results.forEach(element => {

          if (element.customer != null) {
            var row = { 'fname': element.customer.fname, 'lname': element.customer.lname, 'mobile': element.customer.mobile, 'amount_payable': element.amount_payable, 'total_discount': element.total_discount, 'payment_method': element.payment_method != null?element.payment_method.name:("deleted"), 'date': element.customer.date, 'receipt_pdf': element.receipt_pdf ? (<a href={element.receipt_pdf} target="blank">click</a>) : ("") }

            rows.push(row)
          }
        }
        )

        let datatable = { columns: columns, rows: rows }
        this.setState({ datatable: datatable })
      }
    }
    catch (error) {
      // this.errorOccured(500, "erro occurred", error.toString())

    }
  }

  get_next = (response) => {
    try {
      const headers = {
        'Authorization': 'Token ' + sessionStorage.getItem('token')
      }

      axios.get(response, { headers: headers })
        .then(result => {
          this.update_rows(result.data);
          if (result.data.Data.links.next != null) {
            this.get_next(result.data.Data.links.next)
          }
        })
    }
    catch (error) {
      // this.errorOccured(500, "erro occurred", error.toString())

    }

  }

  componentDidMount = () => {
    const headers = {
      'Authorization': 'Token ' + sessionStorage.getItem('token')
    }
    axios.get(window.API_URL+'/receipts/', {
      headers: headers
    })
      .then(response => {
        console.log(response);
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

        // this.errorOccured(500, "error occurred", error.message)
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
          <MDBDataTableV5 className="table-responsive" style={{ backgroundColor: "black", fontSize: "20px", color: "white" }} hover entriesOptions={[10, 20, 25]} entries={10} pagesAmount={4} data={this.state.datatable} searchTop searchBottom={false} />
        </div>
        <div style={{ textAlign: "left", backgroundColor: "black", fontSize: "20px", color: "white" }}>
          <table style={{ width: "100%" }}>
            <tr style={{ color: "red" }}>
              <th>Payment Type</th>
              <th>Amount Paid</th>
            </tr>


            {this.state.payments}
            <tr>
              <th style={{ color: "blue" }}>Total</th>
              <td style={{ color: "blue" }}>{this.state.total_amount}</td>
            </tr>
          </table>
        </div>

      </div>

    )

  }
}
export default Customer;