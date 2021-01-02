<template>
  <navBar />

  <div
    v-if="project"
    class="tile is-ancestor dashboard_default"
    style="margin-top:30px; width:95%; margin:auto"
  >
    <div class="tile is-4 is-vertical is-parent" style="max-height: 100px;">
      <div class="tile is-child box sherlock_tiles">
        <p style="font-size: 7px">project name</p>
        <p class="title">{{ project.name }}</p>
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
            <projectChart :stats="project.last_cycle.cycle" />
          </div>
          <div
            class="panel is-info tile is-child sherlock_tiles"
            style="padding: 0;">
            <projectMenu :project="project" />
          </div>
        </div>
      </div>
      <div class="tile is-child box sherlock_tiles">
        <p style="font-size: 7px;">
          cycle history:
        </p>
        <cycleHistory />
      </div>
    </div>
  </div>
</template>

//
<script>
import NavBar from "@/components/InternalNavBar";
import axios from "axios";

import StackedChart from "@/components/Project/Dashboard/StackedChart";
import CycleHistory from "@/components/Project/Dashboard/CycleHistory";
import ProjectMenu from "@/components/Project/Dashboard/ProjectMenu";

export default {
  components: {
    navBar: NavBar,
    projectChart: StackedChart,
    cycleHistory: CycleHistory,
    projectMenu: ProjectMenu,
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
