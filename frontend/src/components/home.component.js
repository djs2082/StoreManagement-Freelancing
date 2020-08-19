import React, { Component } from 'react';
import '../css/home.css';
import Menu from './menu.component'
import axios from 'axios';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Loader from 'react-loader-advanced';

class Home extends Component {
    constructor(props) {
        super(props)
        let date = new Date();
        if (sessionStorage.getItem('token') === 'undefined' || sessionStorage.getItem('username') === 'undefined') {
            this.props.history.push('/')
        }
        this.state = {
            fname: "",
            lname: "",
            mobile: "",
            payment_method: "",
            birth_day: "",
            items: [
                {
                    "id": 1,
                    "item": "",
                    "brand": "",
                    "size": "",
                    "quantity": 1,
                    "selling_price": 0,
                    "deleteable": false
                }
            ],
            discount_given: 0,
            total_amount: 0,
            total_discount: 0,
            amount_payable: 0,
            payment_options: [],
            categories: [],
            sizes: [],
            errors: [],
            loaded: false,
        }
        const headers = { 'Authorization': 'Token ' + sessionStorage.getItem('token') }

        axios.get(window.API_URL+'/payments/', { headers: headers })
            .then(response => {
                if (response.status == 200) {

                    if (response.data.status == 404) {
                        this.errorOccured(404, response.data.error.error, "No payment options to display")
                    }



                    else if (response.data.status == 200) {
                        this.setState({ payment_options: response.data.Data })

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


        axios.get(window.API_URL+'/items/itemsBrand/', { headers: headers })
            .then(response => {
                if (response.status == 200) {

                    if (response.data.status == 404) {
                        this.errorOccured(404, response.data.error.error, "No Itmes to display")
                    }
                    else if (response.data.status == 200) {
                        let categories = response.data.Data
                        this.setState({ categories: categories })

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


        axios.get(window.API_URL+'/sizes/', { headers: headers })
            .then(response => {
                this.setState({ sizes: response.data.Data })
            })
            .catch(error => {
                this.errorOccured(500, "error occurred", error.message)
            })
        let money = this.find_sum()
        this.setState({ total_amount: money[0], amount_payable: money[2], total_discount: money[1] })

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



    get_pdf = (e) => {
        this.setState({loaded:true})
        var error = false;
        var data={...this.state}
        e.preventDefault();
        if (data.payment_method === "" || data.payment_method === "None") {
            this.errorOccured(404, "erro occurred", "Payment Option is not provided")
            error = true;
        }
        data.items.map(item => {
            if (item.item == "" || item.item == 'Select Item' || item.brand === 'Select Brand' || item.brand === "") {
                this.errorOccured(400, "erro occurred", "something in not provided in item " + item.id)
                error = true;
            }
        })


        this.state.payment_options.map(option => {

            if (option.name === data.payment_method) {
                data.payment_method = option.id
            }
        })

        try {
            if (data.birth_day === "") {
                if (window.confirm('DOB is not provided, Do you wish to continue??')) {
                    data.birth_day = "01-01-2050"
                }
                else {
                    error = true;
                }
            }
            else {

                data.birth_day = this.formatDate(data.birth_day)

            }

        }
        catch (error) {
            this.errorOccured(400, "error occurred in dob", error.message)

        }
        if (error === true) {
            data.birth_day=""
            return false;
        }
        try {
            data.items.map(item => {
                data.categories.map(category => {
                    if (item.item === category.name) {
                        item.item = category.id
                        category.brands.map(brand => {
                            if (brand.name === item.brand) {
                                item.brand = brand.id
                            }

                        })
                    }
                })
            })
        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.message)
        }


        const headers = {
            'Authorization': 'Token ' + sessionStorage.getItem('token')
        }
        console.log(data);
        axios.post(window.API_URL+'/receipts/', data, {
            headers: headers,
        })
            .then(response => {
                this.setState({loaded:false})
                console.log(response)
                if (response.status == 200) {


                    if (response.data.status == 404) {
                        this.errorOccured(404, response.data.error.error, "Error Submitting")
                    }
                    else if (response.data.status == 200) {
                        window.open(window.API_URL + response.data.Data.receipt_link);

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

                this.errorOccured(500, "error occurred", error.toString())
            });
    }




    handleChange = (e) => {
        try {
            var data = e.target.value;
            var money = this.find_sum()
            this.setState({
                [e.target.name]: data
            }, () => { let money = this.find_sum(); this.setState({ total_amount: money[0], amount_payable: money[2], total_discount: money[1] }) })
        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.toString())

        }
    }

    formatDate = (date) => {
        try {
            var d = new Date(date),
                month = '' + (d.getMonth() + 1),
                day = '' + d.getDate(),
                year = d.getFullYear();

            if (month.length < 2)
                month = '0' + month;
            if (day.length < 2)
                day = '0' + day;

            return [year, month, day].join('-');
        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.toString())

        }
    }

    onChange = (birth_day) => {
        try {
            this.setState({ birth_day: birth_day });
        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.toString())
        }
    }


    add_item = () => {
        let item = {
            "id": this.state.items.length + 1,
            "item": "",
            "brand": "",
            "size": "",
            "quantity": 1,
            "selling_price": 0,
            "deleteable": true,
        }
        try {
            let items = [...this.state.items, item];
            this.setState({
                items: items
            });
        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.toString())

        }
    };


    delete_item = (e) => {
        try {
            let key = e.currentTarget.parentNode.parentNode.getAttribute("data-key");
            let items = this.state.items.filter(item => {
                return parseInt(item.id) !== parseInt(key);
            })
            this.setState({ items: items }, () => { let money = this.find_sum(); this.setState({ total_amount: money[0], amount_payable: money[2], total_discount: money[1] }) })

        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.toString())

        }
    }



    update_item = (e) => {
        try {
            let key = e.currentTarget.parentNode.parentNode.parentNode.getAttribute("data-key");
            let name = e.currentTarget.getAttribute("name")
            let value = e.currentTarget.value
            let price = 0
            let quantity = 0
            let actual_cost_price = 0
            let found = false;
            if (value === "") {

                if (name != "size") {
                    return;
                }
            }
            const items = this.state.items.length ? (this.state.items.map(item => {
                if (parseInt(item.id) === parseInt(key)) {
                    item[name] = value;
                    if (name == "brand") {
                        this.state.categories.map(category => {
                            if (item.item === category.name) {

                                category.brands.map(brand => {
                                    if (brand.name === value) {
                                        item.selling_price = brand.actual_cost_price
                                        item.actual_price = brand.cost_price
                                        found = true
                                    }
                                })
                            }
                            if (found == false) {
                                item.selling_price = 0
                                item.actual_price = 0

                            }

                        })
                    }
                }

                return (item)
            })) : ([])
            let money = this.find_sum()

            this.setState({ total_amount: money[0], amount_payable: money[2], total_discount: money[1] })
        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.toString())

        }

    }



    getBrands = (id) => {
        try {
            const brands = this.state.categories.filter(category => {
                return parseInt(category.id) == parseInt(id)
            })
            return (brands[0].brands)
        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.toString())

        }
    }


    find_sum = (quantity, value) => {
        var money = new Array(3).fill(0)
        try {
            var discount = parseInt(this.state.discount_given ? (this.state.discount_given) : 0)
            this.state.items.forEach((item) => {
                let price = parseInt(item.selling_price)
                let quantity = parseInt(item.quantity)
                money[0] = parseInt(money[0]) + parseInt(price) * parseInt(quantity)
            });
            money[1] = Math.round((discount * money[0]) / 100.0)
            money[2] = money[0] - money[1]
            return money;
        }
        catch (error) {
            this.errorOccured(400, "error occurred", error.toString())

        }
    }



    render() {


        const payments = this.state.payment_options.length ? (this.state.payment_options.map(option => {
            return (<option key={option.id}>{option.name}</option>)
        })) : ("");





        const categories = this.state.categories.length ? (this.state.categories.map(category => {
            return (<option key={category.id}>{category.name}</option>)
        })) : ("");



        const sizes = this.state.sizes.length ? (this.state.sizes.map(size => {
            return (<option key={size.id}>{size.name}</option>)
        })) : (" ")

        var Error = this.state.errors.length ? this.state.errors.map(error => {
            return (<div data-key={error.id} className='alert alert-danger alert-dismissible override'>
                <a href="#" onClick={this.deleteError} class="close" data-dismiss="alert" aria-label="close">&times;</a>
                <div><strong>error!</strong> {error.error}</div>
                <div><strong>message</strong> {error.message}</div>
                <div><strong>status</strong> {error.status}</div></div>)
        }) : ("")

        const items = this.state.items.length ? (this.state.items.map(item => {
            const temp = this.state.categories.filter(category => {

                if (item.item == category.name) {
                    return category
                }


            })
            let brands = ""
            try {
                brands = temp[0].brands.length ? (temp[0].brands.map(brand => {
                    return (<option key={brand.id}>{brand.name}</option>)
                })) : (" ")
            }
            catch (e) {
                console.log(e)
            }



            return (
                <div data-key={item.id} className="row">
                    <div className="column">
                        <div style={{ width: "100%" }}><select onChange={this.update_item} type="text" value={item.item} className="form-control item" name="item" placeholder="Item" required>(<option key="-1">Select Itme</option>{categories}</select></div>
                    </div>

                    <div className="column">
                        <div style={{ width: "100%" }}><select onChange={this.update_item} type="text" value={item.brand} className="form-control item" name="brand" placeholder="Brand" required><option key="-1" >Select Brand</option>{brands}</select></div>
                    </div>


                    <div className="column">
                        <div style={{ width: "100%" }}><input onChange={this.update_item} type="text" value={item.size} className="form-control item" name="size" placeholder="Size" list="sizes"></input></div>
                    </div>
                    <div className="column">
                        <div style={{ width: "100%" }}><input autoComplete="off" onChange={this.update_item} type="number" value={item.quantity} className="form-control item" min="1" name="quantity" placeholder="Quantity/Pairs" required /></div>
                    </div>
                    <div className="column">
                        <div style={{ width: "100%" }}><input autoComplete="off" type="number" value={item.actual_price} className="form-control item " min="0" name="actual_price" placeholder="Price" readOnly="True" required /></div>
                    </div>
                    <div className="column">
                        <div style={{ width: "100%" }}><input autoComplete="off" onChange={this.update_item} type="number" value={item.selling_price} className="form-control item " min="0" name="selling_price" placeholder="Price" required /></div>
                    </div>
                    <div className="input-group-postpend column" style={{ width: "10%" }}>
                        {item.deleteable ? (<span onClick={this.delete_item} ><i className="fa fa-times-circle add-btn"></i></span>) : (<span onClick={this.add_item} id="add-item" ><i className="fa fa-plus-circle add-btn"></i></span>)}
                    </div>
                </div>)

        })) : ("");

        return (
            <div className="container">
               <Loader show={this.state.loaded} message={<div class="spinner-border" role="status">
  <span class="sr-only">Loading...</span>
</div>}>

                {Error}
            


                <div className="d-flex justify-content-center h-100">
                    <Menu></Menu>
                    <div style={{ maxWidth: "800px" }} className="card float-left">

                        <div className="card-header">
                            <h3>{window.RECIEPT_MESSAGE}</h3>
                        </div>
                        <div className="col-sm-12 col-sm-offset-4 card-body">
                            <form onSubmit={this.get_pdf} id="login_form">
                                <label style={{ color: "white" }} className="float-left" for="fname"><b>Enter First Name</b></label>

                                <div className="input-group form-group">

                                    <input onChange={this.handleChange} type="text" value={this.state.fname} className="form-control input-sm" id="fname" name="fname" placeholder="First Name" required />
                                </div>
                                <label style={{ color: "white" }} className="float-left" for="lname"><b>Enter Last Name</b></label>

                                <div className="input-group form-group">

                                    <input onChange={this.handleChange} type="text" className="form-control" value={this.state.lname} id="lname" name="lname" placeholder="Last Name" required />
                                </div>
                                <label style={{ color: "white" }} className="float-left" for="mobile"><b>Enter Mobile No:</b></label>

                                <div className="input-group form-group">

                                    <input onChange={this.handleChange} type="tel" value={this.state.mobile} className="form-control" id="mobile" placeholder="Mobile Number" name="mobile" pattern="[0-9]{10}" required />
                                </div>

                                <label style={{ color: "white" }} className="float-left" for="payment"><b>Enter Payment Mode</b></label>

                                <div className="input-group form-group">

                                    <select onChange={this.handleChange} value={this.state.payment_method} id="payment" name="payment_method" className="form-control">
                                        <option> None</option>

                                        {payments}
                                    </select>
                                </div>
                                <label style={{ color: "white" }} className="float-left" for="dob"><b>Enter Date of Birth</b></label>

                                <div className="input-group form-group">

                                    <DatePicker maxDate={new Date()} placeholderText="Enter DOB" dateFormat="dd/MM/yyyy" selected={this.state.birth_day} onChange={this.onChange} />
                                </div>
                                <div id="items-cart">
                                    {items}
                                    <div>
                                    </div>
                                </div>

                                <div className="input-group form-group float-right price-tag">
                                    <div className="input-group-prepend">
                                        <span className="input-group-text"><i className="fa fa-rupee"></i></span>
                                    </div>
                                    <input type="text" className="form-control" value={this.state.amount_payable} readOnly id="amount" />
                                </div>

                                <div className="input-group form-group float-right price-tag">
                                    <div className="input-group-prepend">
                                        <span className="input-group-text"><i className="fa fa-percent"></i></span>
                                    </div>
                                    <input type="number" onChange={this.handleChange} name="discount_given" value={this.state.discount_given} className="form-control" min="0" max="100" />
                                </div>

                                <div className="form-group">
                                    <input type="submit" value="Submit" className="btn-lg login_btn" />
                                </div>

                            </form>
                            <datalist id="sizes">
                                {sizes}
                            </datalist>
                        </div>
                    </div>
                </div>



                </Loader>



            </div>
        )
    }
}
export default Home;
