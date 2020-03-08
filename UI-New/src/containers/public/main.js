import React from 'react';
import { connect } from 'react-redux';

import Input from '../../components/form/input'
import ImageProvider from '../../components/ImageProvider'
import CustomLink from '../../components/navigation/link'
import ButtonProvider from '../../components/common/button'

import logo from '../../assets/logo.png'

import './main.css'
class Login extends React.Component {
  state = {
    name: '',
    password: ''
  }

  onChange = (event) => {
    this.setState({
      name: event.target.value
    })
  }
  

  onChangePassword = (event) => {
    this.setState({
      password: event.target.value
    })
  }
  onClick = () => {
    const { name, password } = this.state;
    if(name === "admin" && password === "admin") {
      this.props.signinAdmin();
    } else {
      this.props.signinPublic(name);
    }
  }

  render() {
    return (
    <div className="container">
      <div>
        <ImageProvider src={logo} className="logo"/>
      </div>
      <form onSubmit={(e) => {e.preventDefault(); this.onClick(e)}}>
        <div>
          <Input
             id="username" name="username" value={this.state.name}
             label="Username" autoFocus onChange={this.onChange} 
            />
        </div>

        <div>
          <ButtonProvider type="submit" label="Sign In" onClick={this.onClick}/>
        </div>
      </form>

    </div>)
  }
}


const mapStateToProps = state => {
  return { parties: state.main.parties };
};

const mapDispatchToProps = (dispatch) => {
  return {
    signinAdmin: () => {
      dispatch({ type: 'SIGNIN_ADMIN_INIT' })
    },
    signinPublic:(email) => {
      dispatch({ type: 'SIGNIN_PUBLIC_INIT', email })
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Login);
