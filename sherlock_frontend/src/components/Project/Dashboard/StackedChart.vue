<template>
  <p style="font-size: 7px;">
    current cycle summary:
  </p>
  <div style="margin: auto">
    <div v-if="casesStats">
      <p style="font-size: 20px">Cycle number 35</p>
      <div class="column">
        <div
          :class="charist_random_class"
          style="height: 20px; margin-left: -59px;"
        ></div>
        <br />
      </div>
      <div class="columns">
        <div class="column" style="font-size: 9px">
          passed: {{ casesStats.stats.total_passed }}
        </div>
        <div class="column" style="font-size: 9px">
          failed: {{ casesStats.stats.total_error }}
        </div>
        <div class="column" style="font-size: 9px">
          blocked: {{ casesStats.stats.total_blocked }}
        </div>
        <div class="column" style="font-size: 9px">
          not executed: {{ casesStats.stats.total_not_executed }}
        </div>
      </div>
    </div>
    <div v-else class="has-text-centered">
      <br>
      <i class="fal fa-info-square" style="font-size:50px"></i>
      <br><br>
      <p class="is-family-monospace	is-size-7 has-text-left">
        This seems like a fresh new project!
      </p>
      <p class="is-family-monospace	is-size-7 has-text-left">
        In order to create a new execution cycle, you need to: <br/>
         1 - create cases by using the menu 'manage cycles' <br />
         2 - click on 'new execution cycle'
      </p>
    </div>
  </div>
</template>

<script>
import Chartist from "chartist";
require("chartist-plugin-legend");

export default {
  props: ["stats"],
  data() {
    return {
      casesStats: this.stats,
      charist_random_class: "project_chartist_" + this._.uid
    };
  },
  methods: {
    chartist() {
      Chartist.Bar(
        "." + this.charist_random_class,
        {
          series: [
            [this.casesStats.total_passed],
            [this.casesStats.total_error],
            [this.casesStats.total_blocked],
            [this.casesStats.total_not_executed]
          ]
        },
        {
          stackBars: true,
          horizontalBars: true
        }
      ).on("draw", function(data) {
        if (data.type === "bar") {
          data.element.attr({
            style: "stroke-width: 20px"
          });
        }
      });
    }
  },
  mounted() {
    if (this.casesStats) {
      this.chartist();
    }
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
