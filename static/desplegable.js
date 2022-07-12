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
    }

elements = ['1','2','3','4','5','6','7','8','9','10','11']
let i = 0
const elementsList = elements.map((element) => {
    if (!playerNum.includes(element)) {
        return element
    } 
})
for (element of elementsList){
    if (element !== undefined ) {
        document.write(`<option value="${element}">${element}</option>`);
    } 
}
