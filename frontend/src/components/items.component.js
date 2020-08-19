import React, { Component } from 'react'
import { MDBDataTableV5 } from 'mdbreact';
import Menu from './menu.component'
import axios from 'axios';

class Items extends Component {
  constructor(props) {
    super(props);
    if (sessionStorage.getItem('token') === 'undefined' || sessionStorage.getItem('username') === 'undefined') {
      this.props.history.push('/')
    }
    this.state = {
      datatable: {
        columns: [
          {
            label: 'Item',
            field: 'item',
            width: 150,
          },
          {
            label: 'BrandName',
            field: 'name',
            width: 270,
          },
          {
            label: 'Quantity',
            field: 'quantity',
            width: 200,
          },
          {
            label: 'Remaining',
            field: 'remaining',
            width: 200,
          },
          {
            label: 'Purchasing Price',
            field: 'price',
            width: 200,
          },
          {
            label: 'GST',
            field: 'gst',
            width: 200,
          },
          {
            label: 'Transport Charge',
            field: 'transport_charge',
            width: 200,
          },
          {
            label: 'Selling Price',
            field: 'cost_price',
            width: 200,
          },
          {
            label: 'Discount',
            field: 'intitial_discount',
            width: 200,
          },
          {
            label: 'Payable',
            field: 'actual_cost_price',
            width: 200,
          },


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

  componentDidMount = () => {
    const headers = {
      'Authorization': 'Token ' + sessionStorage.getItem('token')
    }
    axios.get(window.API_URL+'/brands/', {
      headers: headers
    })
      .then(response => {
        console.log(response);
        if (response.status == 200) {

          if (response.data.status == 404) {
            this.errorOccured(404, response.data.error.error, "Error")
          }

          else if (response.data.status == 200) {
            var items = response.data.Data.map(item => {
              return ({ 'item': item.item.name, 'name': item.name, 'quantity': item.initial_quantity, 'remaining': item.quantity, 'cost_price': item.cost_price,'price': item.price, 'intitial_discount': item.initial_discount, 'actual_cost_price': item.actual_cost_price, 'gst': item.gst, 'transport_charge': item.transport_charge })
            })
            let columns = this.state.datatable.columns
            let datatable = { columns: columns, rows: items }
            this.setState({ datatable: datatable })


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
        <Menu />
        {Error}
        <div style={{ backgroundColor: "black", fontSize: "15px", color: "green" }}>
          <MDBDataTableV5 className="table-responsive" style={{ textAlign: "left", backgroundColor: "black", fontSize: "20px", color: "white" }} hover entriesOptions={[10, 20, 25]} entries={10} pagesAmount={4} data={this.state.datatable} searchTop searchBottom={false} />
        </div>
      </div>

    )

  }
}
export default Items;