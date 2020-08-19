import React from 'react';
import './App.css';
import Login from './components/login.component.js';
import Home from './components/home.component.js';
import Menu from './components/menu.component.js'
import Customer from './components/customer.component'
import Graph from './components/statistics.component'
import Sale from './components/sale.component'
import Items from './components/items.component'
import 'bootstrap/dist/css/bootstrap.min.css'
import {BrowserRouter,Route,Switch, Router} from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
    <div className="App">
     <Route exact path='/menu' component={Menu}></Route>
     <Route exact path='/home' component={Home}></Route>
     <Route exact path='/customer' component={Customer}></Route>
     <Route exact path='/sale' component={Sale}></Route>
     <Route exact path='/statistics' component={Graph}></Route>
     <Route exact path='/items' component={Items}></Route>


     <Route exact path='/' component={Login}></Route>

    </div>
    </BrowserRouter>
  );
}

export default App;
