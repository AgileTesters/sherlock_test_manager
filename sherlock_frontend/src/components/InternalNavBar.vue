<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link class="navbar-item" :to="{ path: '/dashboard' }">
        <img src="../assets/logo_navbar.png" />
      </router-link>
      <a
        role="button"
        class="navbar-burger burger"
        aria-label="menu"
        aria-expanded="false"
        data-target="navbarSherlock"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="navbarSherlock" class="navbar-menu">
      <div class="navbar-end">
        <a class="navbar-item">
          <i class="fal fa-home" style="text-align: center;font-size: x-large;">
            <br />
            <span
              style="font-size:15px; font-family: Nunito; text-align: center;"
            >
              Home</span
            >
          </i>
        </a>
        <div class="navbar-item has-dropdown is-hoverable">
          <a class="navbar-link">
            <i
              class="fal fa-users-cog"
              style="text-align: center;font-size: x-large;"
            >
              <br />
              <span
                style="font-size:15px; font-family: Nunito; text-align: center;"
                >Teams</span
              >
            </i>
          </a>
          <div class="navbar-dropdown is-right">
            <a class="navbar-item">
              TO BO IMPLEMENTED
            </a>
            <hr class="navbar-divider" />
            <a class="navbar-item">
              x
            </a>
          </div>
        </div>

        <!-- MENU FOR USER  -->
        <div class="navbar-item has-dropdown is-hoverable">
          <a class="navbar-link">
            <i
              class="fal fa-desktop-alt"
              style="text-align: center;font-size: x-large;"
            >
              <br />
              <span
                style="font-size:15px; font-family: Nunito; text-align: center;"
                >Projects</span
              >
            </i>
          </a>
          <div class="navbar-dropdown is-right">
            <router-link class="navbar-item" :to="{ path: '/dashboard' }">
              All projects
            </router-link>
            <hr class="navbar-divider" />
            <createProjectModal />
          </div>
        </div>

        <div class="navbar-item has-dropdown is-hoverable">
          <a class="navbar-link">
            <i
              class="fal fa-address-card"
              style="text-align: center;font-size: x-large;"
              ><br />
              <span
                style="font-size:15px; font-family: Nunito; text-align: center;"
                >Profile</span
              >
            </i>
          </a>
          <div class="navbar-dropdown is-right">
            <a class="navbar-item">
              Profile
            </a>
            <a class="navbar-item" @click="logout">
              Logout
            </a>
            <hr class="navbar-divider" />
            <a
              class="navbar-item"
              href="https://github.com/AgileTesters/sherlock_test_manager/issues"
            >
              Report an issue
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
import createProjectModal from "@/components/Project/CreateProjectModal";

export default {
  components: {
    createProjectModal
  },
  data() {
    return {};
  },
  mounted() {},
  methods: {
    logout() {
      localStorage.removeItem('authentication_data');
      this.$router.push('/login');
    }
  }
};
</script>
<style>
.navbar-item img {
  max-height: 2.75rem !important;
}
</style>
