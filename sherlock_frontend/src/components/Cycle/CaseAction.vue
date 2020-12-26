<template>
  <div>
      <ul style="display:inline-flex;">
        <li @click="approve()" v-bind:class="{ 'approved': caseState == 'approved'  }"><i class="far fa-check-square is-clickable"></i></li>
        <li @click="reprove()" v-bind:class="{ 'reproved': caseState == 'reproved'  }"><i class="far fa-check-square is-clickable"></i></li>
        <li @click="block()" v-bind:class="{ 'blocked': caseState == 'blocked'  }"><i class="far fa-check-square is-clickable"></i></li>
        <li @click="resetStatus()"><i class="far fa-check-square is-clickable"></i></li>
      </ul>
  </div>
</template>
<script>
export default {
  props: {
    caseId: Number,
    projectId: Number,
    state: null,
  },
  data() {
    return {
      caseState: this.state
    };
  },
  methods: {
    approve() {
        this.caseState = 'approved'
    },
    reprove() {
      this.caseState = 'reproved'
    },
    block() {
      this.caseState = 'blocked'
    },
    resetStatus() {
      this.caseState = null
    }
  },
  mounted() {

  }
};
</script>
<style>

  li {
    padding: 0px 10px 0px 0px !important;
  }

  .approved{
    color: green;
  }
  .reproved{
    color: red;
  }
  .blocked{
    color: darkorange
  }

  .far {
    font-weight: 600 !important;
  }

</style>
