function upload(e) {
    let file = $(e).val().split("\\").pop()
    $('.custom-file-label').addClass("selected").html(file)
}

function addFactor(add) {
    $('.factor-root').append("<div class='container'>" +
        "<div class='input-group mb-3 p-3'>" +
        "<input type='text'  name='factor_name" + $('.container').length + "' class='form-control' aria-label='Default'" +
        "aria-describedby='inputGroup-sizing-default' value='"
        + add.parentNode.parentNode.children.item(1).value + "' >" +
        "   <div class='input-group-append'>" +
        "<button class='btn  btn-danger p-8' type='button' " +
        "onclick='removeFactor(this)'>Delete factor</button>" +
        " </div>" +
        "</div>" +
        "<div class='input-group mb-3 p-3'>" +
        "<span class='material-icons'" +
        "style='margin-left: 50px; align-items: center;font-size: 36px'>add_circle</span>" +
        "<input type='text'  class='form-control col-md-pull-8' aria-label='Default'" +
        "aria-describedby='inputGroup-sizing-default' placeholder='Level name'" +
        "<div class='input-group-append'>" +
        "<button class='btn  btn-success p-8' onclick='addLevel(this)' type='button'>Add level</button>" +
        "</div>" +
        "</div>" +
        "</div>")
}

function addLevel(level) {
    let factorLevels = level.parentNode.parentNode.children;
    let levelPlace = factorLevels[factorLevels.length - 1]

    $(level.parentNode).before(
        "<div class='input-group p-3'>" +
        "<input style='margin-left: 50px' type='text' class='form-control col-md-pull-8''" +
        "aria-label='Default'" +
        "aria-describedby='inputGroup-sizing-default' value='" +
        level.parentNode.children.item(1).value + "'>" +
        "<div class='input-group-append'>" +
        "<button class='btn  btn-danger p-8' onclick='removeLevel(this)' " +
        "type='button'>Delete level</button>" +
        "</div>" +
        "</div>", $(levelPlace)
    )
}


function removeFactor(factor) {
    factor.parentNode.parentNode.parentElement.parentNode.removeChild(factor.parentNode.parentNode.parentElement)
}


function removeLevel(level) {
    level.parentNode.parentNode.parentNode.removeChild(level.parentNode.parentNode)
}

function gatherFactors() {
    let factors = []
    for (let container of document.querySelector('.factor-root').childNodes) {
        let factor = {level: []}
        for (let i = 0; i < container.children.length - 1; i++) {
            if (i === 0) {
                factor.name = container.children[i].children[0].value;
                continue;
            }
            factor.level.push({name: container.children[i].children[0].value});
        }
        factors.push(factor);
    }
    return factors;
}

