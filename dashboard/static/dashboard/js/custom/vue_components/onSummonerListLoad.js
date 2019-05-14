function onSummonerListLoad() {

    let query_getTopSummoners =
        `
        query {
            topSummoners {
                summonerName
                rankedSolo {
                  tier
                  rank
                  rankNumber
                  lp
                  leagueName
                  wins
                  losses
                  ringValues
                }
              }
              latestUpdatedSummoners {
                summonerName
                lastUpdated
              }
            }
        `;

    let query_addSummoner =
        `
        mutation($summonerName: String) {
          createSummoner(input: {
            summonerName: $summonerName
          }) {
            created
            message
            summoner {
              summonerName
              rankedSolo {
                tier
                rank
                rankNumber
                lp
                leagueName
                wins
                losses
                ringValues
              }
            }
          }
        }
        `;

    let SummonerListVM = new Vue({
        delimiters: ['[[', ']]'],
        el: '#summoners',
        data: {
            // Player Lists
            topPlayers: [],
            latestPlayers: [],

            // Misc. Data
            addSummonerName: '',

            // Loading Flags
            topPlayersLoading: true,
            latestPlayersLoading: true,

            // Error Handling
            isError: false,
            errorMessage: '',
        },
        methods: {
            getSummonerLists() {
                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = 'X-CSRFToken';
                axios({
                    url: '/graphql',
                    method: 'post',
                    data: {
                        query: query_getTopSummoners,
                        variables: {},
                    }
                }).then((response) => {
                    SummonerListVM.topPlayers = response.data.data.topSummoners;
                    SummonerListVM.latestPlayers = response.data.data.latestUpdatedSummoners;

                    SummonerListVM.topPlayersLoading = false;
                    SummonerListVM.latestPlayersLoading = false;
                });
            },
            addSummoner() {
                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = 'X-CSRFToken';
                axios({
                    url: '/graphql',
                    method: 'post',
                    data: {
                        query: query_addSummoner,
                        variables: {
                            summonerName: SummonerListVM.addSummonerName
                        },
                    }
                }).then((response) => {
                    console.log(response);
                   if (!response['created']){
                       errorVM.isError = true;
                       errorVM.errorMessage = response['message'];
                   }
                });
            },
        },
        mounted() {
            this.getSummonerLists()
        }
    });
}