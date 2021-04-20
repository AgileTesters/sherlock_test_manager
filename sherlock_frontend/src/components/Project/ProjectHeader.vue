<template>
	<div
		class="tile is-ancestor dashboard_default"
		style="margin-top:30px; width:95%; margin:auto"
	>
		<div class="tile is-4 is-vertical is-parent" style="max-height: 100px;">
			<div class="tile is-child box sherlock_tiles">
				<p style="font-size: 7px">project name</p>
				<p class="title">{{ projectName }}</p>
			</div>
		</div>
		<div class="tile is-parent is-vertical">
			<div class="tile is-child box sherlock_tiles">
				<nav class="navbar" role="navigation" aria-label="main navigation">
					<div id="navbarSherlock" class="navbar-menu">
						<div class="navbar-end">
							<a class="navbar-item">
								<i
									class="fal fa-home"
									style="text-align: center;font-size: x-large;"
								>
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
			</div>
		</div>
	</div>
</template>
<script>
export default {
	props: {
		projectId: Number,
		projectName: String,
		state: null
	},
	data() {
		return {
			caseState: this.state
		};
	},
	methods: {
		approve() {
			this.caseState = "approved";
		},
		reprove() {
			this.caseState = "reproved";
		},
		block() {
			this.caseState = "blocked";
		},
		resetStatus() {
			this.caseState = null;
		}
	},
	mounted() {}
};
</script>
<style></style>
