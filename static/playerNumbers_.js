if (typeof window !== 'undefined') {

function playerList(count) {
    while (count <= 11 ) {  
        if (document.querySelector(`.player_number${count}`)) {
            playerNum.push(document.querySelector(`.player_number${count}`).value)
        } else {
            console.log('no encontrado')
        }
        count = count + 1
    }
    return playerNum
}
var playerNum = []
var count = 1
playerList(count)
console.log(playerNum)
}
console.log(playerNum)

