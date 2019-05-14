function onSummonerProfileLoad(summonerName) {
    // const axios = require("axios") Figure out how this works.

    // Get font size for username depending on username length.
    let nameFontSize = getFontSize(document.documentElement.clientWidth, summonerName);

    let query_getSummonerInfo =
        `
            query SummonerProfile($summonerName: String, $games: Int){
              summoner(summonerName: $summonerName) {
                summonerName
                profileIconId
                summonerLevel
                lastUpdated
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
                rankedFlex5 {
                  tier
                  rank
                  rankNumber
                  lp
                  leagueName
                  wins
                  losses
                  ringValues
                }
                rankedFlex3 {
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
              summonerPlayers(summonerName: $summonerName, games: $games){
                match {
                  gameId
                  queue
                  gameDurationTime
                  timeago
                  timestamp
                }
                champion {
                  key
                  name
                  champId
                }
                win
                kills
                deaths
                assists
                kdaAverage
                killParticipation
                totalMinionsKilled
                csPmin
                item0 {
                  itemId
                  name
                }
                item1 {
                  itemId
                  name
                }
                item2 {
                  itemId
                  name
                }
                item3 {
                  itemId
                  name
                }
                item4 {
                  itemId
                  name
                }
                item5 {
                  itemId
                  name
                }
                item6 {
                  itemId
                  name
                }
                spell1Id {
                  name
                  imageFull
                }
                spell2Id {
                  name
                  imageFull
                }
                perk0 {
                  name
                  icon
                }
                perkSubStyle
                perk4 {
                  name
                }
              }
            }
        `;

    let summonerProfileVM = new Vue({
        delimiters: ['[[', ']]'],
        el: '#summonerProfile',
        data: {
            // Object Data
            summoner: {},
            matches: [],

            // Misc. Data
            nameFontSize: nameFontSize,

            // Flags
            isError: false,

            //Loading
            playerLoading: false,
            matchLoading: false,
        },
        computed: {},
        methods: {
            getSummonerInfo() {
                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = 'X-CSRFToken';
                axios({
                    url: '/graphql',
                    method: 'post',
                    data: {
                        query: query_getSummonerInfo,
                        variables: {
                            summonerName: summonerName,
                            games: 10
                        },
                    }
                }).then((summonerProfileInfo) => {
                    summonerProfileVM.summoner = summonerProfileInfo.data.data.summoner;
                    summonerProfileVM.matches = summonerProfileInfo.data.data.summonerPlayers;
                    console.log(summonerProfileInfo);

                });
            },
            updateSummoner() {
                console.log('Under Maintenance.');
            }
        },
        mounted() {
            this.getSummonerInfo()
        }
    });

    $("#summoner-menu > .general").click(function () {
        $("#summoner-content-wrapper").attr("class", "general");
        $("#summoner-menu > .selector").attr("class", "selector");
        $("#summoner-menu").attr("class", "");
    });

    $("#summoner-menu > .matches").click(function () {
        $("#summoner-content-wrapper").attr("class", "matches");
        $("#summoner-menu > .selector").attr("class", "selector s_matches");
        $("#summoner-menu").attr("class", "s_matches");
    });

    $("#summoner-menu > .champions").click(function () {
        $("#summoner-content-wrapper").attr("class", "champions");
        $("#summoner-menu > .selector").attr("class", "selector s_champions");
        $("#summoner-menu").attr("class", "s_champions");
    });

    $("#summoner-menu > .achievements").click(function () {
        $("#summoner-content-wrapper").attr("class", "achievements");
        $("#summoner-menu > .selector").attr("class", "selector s_achievements");
        $("#summoner-menu").attr("class", "s_achievements");
    });
}

function getFontSize(viewport, summonerName) {
    if (viewport >= 768) {
        if (summonerName.length > 14) {
            return '5rem';
        } else if (summonerName.length > 10) {
            return '6rem';
        } else {
            return '7rem';
        }
    } else {
        if (summonerName.length > 14) {
            return '1.5rem';
        } else if (summonerName.length > 10) {
            return '2.5rem';
        } else {
            return '3.5rem';
        }
    }
}