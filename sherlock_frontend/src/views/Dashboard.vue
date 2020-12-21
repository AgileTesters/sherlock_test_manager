<template>
  <navBar />
  <div class="columns is-multiline">
    <div class="column" v-for="item in projects" v-bind:key="item">
      <project :project="item"></project>
    </div>
  </div>
</template>

//
<script>
import NavBar from "@/components/InternalNavBar";
import Project from "@/components/Dashboard/Project";
import axios from "axios";

export default {
  components: {
    navBar: NavBar,
    project: Project
  },
  data() {
    return {
      projects: null
    };
  },
  methods: {
    async fecth_projects() {
      var tokenData = JSON.parse(
        window.localStorage.getItem("authentication_data")
      );
      var requestOptions = {
        method: "get",
        url: "/dashboard/",
        headers: {
          Authorization: "Bearer " + tokenData.token
        }
      };
      await axios(requestOptions)
        .then(response => {
          this.projects = response.data.projects;
        })
        .catch(error => {
          this.error = error;
        });
    }
  },
  async mounted() {
    await this.fecth_projects();
  }
};
</script>
<style>
html {
  background-color: #eff1f3 !important;
  font-family: Avenir, Helvetica, Arial, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
