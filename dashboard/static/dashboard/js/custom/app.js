function onSummonerProfileLoad() {
    // const axios = require("axios") Figure out how this works.

    let summonerName = $('#summonerName').val();

    // Get font size for username depending on username length.
    let nameFontSize = '';
    if (document.documentElement.clientWidth >= 768) {
        if (summonerName.length > 14) {
            nameFontSize = '5rem';
        } else if (summonerName.length > 10) {
            nameFontSize = '6rem';
        } else {
            nameFontSize = '7rem';
        }
    } else {
        if (summonerName.length > 14) {
            nameFontSize = '1.5rem';
        } else if (summonerName.length > 10) {
            nameFontSize = '2.5rem';
        } else {
            nameFontSize = '3.5rem';
        }
    }

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

    let errorVm = new Vue({
        delimiters: ['[[', ']]'],
        el: '#errors',
        data: {
            isError: false,
            errorMessage: '',
        }
    });

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
    })
}

function oldSummonerLoad() {
    let summonerName = $('#summonerName').val();

    let errorVm = new Vue({
        delimiters: ['[[', ']]'],
        el: '#errors',
        data: {
            isError: false,
            errorMessage: '',
        }
    });

    let vm = new Vue({
        delimiters: ['[[', ']]'],
        el: '#profile',
        data: {
            remaining_games: 0,
            matchLoading: true,
            newGamesLoading: false,
            playerLoading: true,
            isEmpty: false,
            isError: false,
        },
        computed: {
            sortedMatches() {
                return vm.match_list.sort(function (a, b) {
                    let x = a['match']['timestamp'];
                    let y = b['match']['timestamp'];
                    return ((x > y) ? -1 : ((x < y) ? 1 : 0));
                });
            }
        },
        methods: {
            updateSummoner: async function (event) {
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.xsrfHeaderName = 'X-CSRFToken'
                vm.matchLoading = true;
                vm.playerLoading = true;
                await axios.get('/api/summoners/' + summonerName + '?isUpdate=True')
                    .then(async function (updateResponse) {
                        console.log(updateResponse)
                        if (updateResponse.data['isError']) {
                            errorVm.isError = true;
                            errorVm.errorMessage = updateResponse.data['errorMessage'] === 'Rate limit exceeded' ? 'Server under heavy load, try again soon.' : updateResponse.data['errorMessage'];
                            vm.isError = true;
                            vm.matchLoading = false;
                            vm.playerLoading = false;
                            setTimeout(function () {
                                errorVm.isError = false;
                            }, 3000);
                            setTimeout(function () {
                                vm.isError = false;
                            }, 3200);
                            console.log(updateResponse.data)
                        } else {
                            console.log(updateResponse.data);
                            vm.summoner = updateResponse.data['summonerInfo']
                            vm.last_updated = moment(updateResponse.data['summonerInfo'].date_updated).fromNow()
                            vm.playerLoading = false;
                            await axios.get('/api/summoners/{{ summoner.summonerName }}').then(response => {
                                if (updateResponse.data['newMatches'].length == 0) {
                                    vm.matchLoading = false;
                                } else {
                                    console.log(updateResponse.data['newMatches']);
                                    vm.remaining_games = updateResponse.data['newMatches'].length;
                                    vm.createNewMatches(updateResponse.data['newMatches']);
                                }
                            })
                        }
                    })
            },
            async createNewMatches(newMatchArray) {
                try {
                    await axios.post('/api/matches/', {
                        'gameId': newMatchArray[0]['gameId'],
                    }).then(response => {
                        if (response.data['isError']) {
                            errorVm.isError = true;
                            errorVm.errorMessage = response.data['errorMessage'] == 'Rate limit exceeded' ? 'Server under heavy load, try again soon.' : response.data['errorMessage'];
                            vm.isError = true;
                            vm.matchLoading = false;
                            setTimeout(function () {
                                errorVm.isError = false;
                            }, 3000);
                            setTimeout(function () {
                                vm.isError = false;
                            }, 3200);
                            return false;
                        } else if (response.data['ignore']) {
                            vm.matchLoading = false;
                            return false;
                        } else {
                            axios.get('/api/players/?match=' + newMatchArray[0]['gameId'] + '&player=' + vm.summoner.summonerId).then(playerResponse => {
                                response.data['newMatch']['summonerPrime'] = playerResponse.data['results'][0];
                                response.data['newMatch']['timeAgo'] = moment(response.data['newMatch']['timestamp']).fromNow();
                                vm.match_list.push(response.data['newMatch']);
                                newMatchArray.shift();
                                vm.remaining_games = newMatchArray.length;
                                vm.matchLoading = false;
                                if (newMatchArray.length > 0) {
                                    vm.newGamesLoading = true;
                                    vm.createNewMatches(newMatchArray);
                                } else {
                                    vm.newGamesLoading = false;
                                }
                            })
                        }
                    });
                } catch (e) {
                    console.log(e)
                }
            }
        },
        mounted() {
            this.getSummonerInfo()
        }
    })
}

$(document).ready(function () {
    $(".sidebar-dropdown > a").click(function () {
        $(".sidebar-submenu").slideUp(200);
        if (
            $(this)
                .parent()
                .hasClass("active")
        ) {
            $(".sidebar-dropdown").removeClass("active");
            $(this)
                .parent()
                .removeClass("active");
        } else {
            $(".sidebar-dropdown").removeClass("active");
            $(this)
                .next(".sidebar-submenu")
                .slideDown(200);
            $(this)
                .parent()
                .addClass("active");
        }
    });

    $(".acc-options").on("click", function (e) {
        $(this).toggleClass("open");
        e.stopPropagation()
    });
    $(document).on("click", function (e) {
        if ($(e.target).is(".acc-options") === false) {
            $(".acc-options").removeClass("open");
        }
    });

    $("#summoner-menu > .general").click(function () {
        $("#summoner-content-wrapper").attr("class", "general");
        $("#summoner-menu > .selector").attr("class", "selector");
        $("#summoner-menu").attr("class", "");
    })
    $("#summoner-menu > .matches").click(function () {
        $("#summoner-content-wrapper").attr("class", "matches");
        $("#summoner-menu > .selector").attr("class", "selector s_matches");
        $("#summoner-menu").attr("class", "s_matches");
    })
    $("#summoner-menu > .champions").click(function () {
        $("#summoner-content-wrapper").attr("class", "champions");
        $("#summoner-menu > .selector").attr("class", "selector s_champions");
        $("#summoner-menu").attr("class", "s_champions");
    })
    $("#summoner-menu > .achievements").click(function () {
        $("#summoner-content-wrapper").attr("class", "achievements");
        $("#summoner-menu > .selector").attr("class", "selector s_achievements");
        $("#summoner-menu").attr("class", "s_achievements");
    })
});
