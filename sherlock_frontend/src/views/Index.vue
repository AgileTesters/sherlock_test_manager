<template>
  <div class="columns">
    <div class="column" style="background-color: #f0f1ef; text-align: center;">
      <img
        src="../assets/sherlock_thinking.png"
        style="width: 80%; padding: 10%"
      />
    </div>
    <div class="column" style="padding-top:15%">
      <div v-if="this.currentComponent == 'login'">
        <p style="padding-bottom:20px">
          let's go find some bugs together?
        </p>
        <div class="field">
          <div class="control has-icons-left has-icons-right">
            <input
              class="input"
              type="text"
              placeholder="email"
              style="width:50%"
              id="email"
              v-model="login.email"
            />
            <span class="icon is-small is-left">
              <i class="fal fa-id-badge"></i>
            </span>
          </div>
        </div>

        <div class="field">
          <div class="control has-icons-left has-icons-right">
            <input
              class="input"
              type="password"
              placeholder="password"
              style="width:50%"
              id="password"
              v-model="login.password"
            />
            <span class="icon is-small is-left">
              <i class="fal fa-lock"></i>
            </span>
            <!-- <span class="icon is-small is-right">
                  <i class="fas fa-exclamation-triangle"></i>
                </span> -->
          </div>
        </div>
        <div class="field is-grouped">
          <div class="control">
            <button
              class="button"
              style="color:#969696; margin-right:10px"
              title="sign-in"
              v-on:click="handleLogin()"
            >
              <i class="fal fa-sign-in-alt"></i>
            </button>

            <button
              class="button"
              style="color:#969696;"
              title="register user"
              v-on:click="swapComponent('register')"
            >
              <i class="fal fa-user-plus"></i>
            </button>

            <p v-if="error" id="login_display_msg" class="help is-danger">
              {{ error }}
            </p>
          </div>
        </div>
      </div>
      <div v-else>
        <p style="padding-bottom:20px">
          just a few inputs and you are go to go!
        </p>
        <div class="field">
          <div class="control has-icons-left has-icons-right">
            <input
              class="input"
              type="text"
              placeholder="name"
              style="width:50%"
              id="name"
              v-model="register.name"
            />
            <span class="icon is-small is-left">
              <i class="fal fa-user"></i>
            </span>
          </div>
        </div>
        <div class="field">
          <div class="control has-icons-left has-icons-right">
            <input
              class="input"
              type="text"
              placeholder="email"
              style="width:50%"
              id="email"
              v-model="register.email"
            />
            <span class="icon is-small is-left">
              <i class="fal fa-at"></i>
            </span>
          </div>
          <!--<p class="help is-success">This username is available</p>-->
        </div>

        <div class="field">
          <div class="control has-icons-left has-icons-right">
            <input
              class="input"
              type="password"
              placeholder="password"
              style="width:50%"
              id="password"
              v-model="register.password"
            />
            <span class="icon is-small is-left">
              <i class="fal fa-lock"></i>
            </span>
          </div>
        </div>
        <div class="field is-grouped">
          <div class="control">
            <button
              class="button"
              style="color:#969696; margin-right:10px"
              title="register user"
              v-on:click="handleRegister('login')"
            >
              <i class="fal fa-user-plus"></i>
            </button>
            <button
              class="button"
              style="color:#969696;"
              title="back to login"
              v-on:click="swapComponent('login')"
            >
              back to login
            </button>

            <p v-if="error" id="login_display_msg" class="help is-danger">
              {{ error }}
            </p>
          </div>
        </div>
        <Register />
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "index",
  data() {
    return {
      login: {
        email: null,
        password: null
      },
      register: {
        name: null,
        email: null,
        password: null
      },
      currentComponent: "login",
      error: null
    };
  },
  methods: {
    swapComponent: function(currentComponent) {
      this.currentComponent = currentComponent;
      this.error = null;
    },
    handleLogin: function() {
      if (!this.login.email || !this.login.password) {
        this.error = "Please fill all the inputs to login";
        return false;
      }
      var auth = {};
      var requestOptions = {
        method: "post",
        url: "/login",
        headers: {
          Authorization:
            "Basic " + btoa(this.login.email + ":" + this.login.password)
        }
      };
      axios(requestOptions)
        .then(response => {
          auth = response.data;
          window.localStorage.setItem(
            "authentication_data",
            JSON.stringify(auth)
          );
          this.$router.push({ path: "/dashboard" });
        })
        .catch(error => {
          this.error = error;
        });
    },
    handleRegister: function() {
      if (
        !this.register.email ||
        !this.register.password ||
        !this.register.name
      ) {
        this.error = "Please fill all the inputs to register a user";
        return false;
      }
      var requestOptions = {
        method: "post",
        url: "/users/new",
        data: {
          name: this.register.name,
          email: this.register.email,
          password: this.register.password
        }
      };
      axios(requestOptions)
        .then(response => {
          // TODO: add visual feedback that is working
          if (response.data.message != "USER_CREATED") {
            this.error = response.data.message;
          } else {
            this.swapComponent("login");
          }
        })
        .catch(error => {
          this.error = error;
        });
    },
    created: function() {
      window.localStorage.removeItem("auth");
    }
  }
};
</script>
