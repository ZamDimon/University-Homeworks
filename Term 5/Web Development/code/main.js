const NUMBERS_TO_DISPLAY = 10
const MILISECONDS_TO_WAIT = 1000

async function fn (a) {
    await new Promise (r => setTimeout(r, MILISECONDS_TO_WAIT * (NUMBERS_TO_DISPLAY - a)))
    return a
}

async function main () {
    for (var i = 0; i < NUMBERS_TO_DISPLAY; i++) {
        let result = await fn(i)
        console.log(result)
    }
}

main()