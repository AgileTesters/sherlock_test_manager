<template>
  <navBar />

  <div
    v-if="project"
    class="tile is-ancestor dashboard_default"
    style="margin-top:30px; width:85%; margin:auto"
  >
    <div class="tile is-4 is-vertical is-parent">
      <div class="tile is-child box sherlock_tiles">
        <p style="font-size: 7px">{{ project.name }}</p>
        <p class="title">PIX</p>
      </div>
      <div class="tile is-child box sherlock_tiles">
        <p style="font-size: 7px">description:</p>
        <p style="font-weight: 300;">
          {{ project.description }}
        </p>
      </div>
    </div>
    <div class="tile is-parent is-vertical">
      <div class="tile is-child">
        <div class="tile is-parent" style="padding: 0;">
          <div
            class="tile is-parent box is-8 sherlock_tiles"
            style="margin-right: 20px; margin-bottom: 0px;"
          >
            <projectChart :stats="project.last_cycle.cycle"/>
          </div>
          <div class="panel is-info tile is-child sherlock_tiles" style="padding: 0;">
            <p class="panel-heading sherlock_tiles">
              actions menu
            </p>
            <router-link class="panel-block" :to="{ name: 'manageCases', params: { projectId: project.id}}">
              <span class="panel-icon">
                <i class="fas fa-book" aria-hidden="true"></i>
              </span>
              manage Cases
            </router-link>
            <a class="panel-block">
              <span class="panel-icon">
                <i class="fas fa-code-branch" aria-hidden="true"></i>
              </span>
              execute test
            </a>

                <div v-if="project.last_cycle.cycle || project.last_cycle.closed">
                  <a class="panel-block">
                    <span class="panel-icon">
                      <i class="fas fa-code-branch" aria-hidden="true"></i>
                    </span>
                    stop cycle
                  </a>
                </div>
                <div v-else>
                  <a class="panel-block">
                    <span class="panel-icon">
                      <i class="fas fa-code-branch" aria-hidden="true"></i>
                    </span>
                    new cycle

                  </a>
                </div>
          </div>
        </div>
      </div>
      <div class="tile is-child box sherlock_tiles">
        <p style="font-size: 7px;">
          cycle history:
        </p>
          <p class="title">
            d
          </p>
      </div>
    </div>
  </div>
</template>

//
<script>
import NavBar from "@/components/InternalNavBar";
import axios from "axios";

import StackedChart from "@/components/Project/Dashboard/StackedChart";

export default {
  components: {
    navBar: NavBar,
    projectChart: StackedChart
  },
  data() {
    return {
      project: null
    };
  },
  methods: {
    async fecth_project() {
      var requestOptions = {
        method: "get",
        url: "/projects/project/" + this.$route.params.projectId
      };
      await axios(requestOptions)
        .then(response => {
          this.project = response.data;
        })
        .catch(error => {
          this.error = error;
        });
    }
  },
  async mounted() {
    await this.fecth_project();
    console.log(this.project);
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
