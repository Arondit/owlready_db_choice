const requirements = [
    {
        text: 'СУБД может работать даже без сервера',
        name: 'no_needs_server',
    },
    {
        text: `
            Должна нормально работать «из коробки»: 
            важно, когда нет возможности нанять опытного специалиста по базам данных
        `,
        name: 'works_from_box',
    },
    {
        text: `Должна быстро работать с текстом: например, в поисковых системах или при анализе текста`,
        name: 'working_with_texts',
    },
    {
        text: `Должна быть бесплатной: не всегда возможно использовать платные решения`,
        name: 'must_be_free',
    },
    {
        text: `
            Должна отвечать одинаково быстро независимо от географии: 
            если пользователи распределены по всему миру, то расположение сервера очень важно. 
            СУБД должна быть в состоянии безболезненно разбиваться на несколько изолированных серверов
        `,
        name: 'geo_independency',
    },
    {
        text: `Нужно хранить огромные данные: речь о данных, которые не помещаются на одном сервере`,
        name: 'store_big_data',
    },
    {
        text: `Должна отвечать как можно быстрее: скорость отклика является критичной`,
        name: 'fast_response',
    },
    {
        text: `
            Нужно анализировать настолько огромные данные, 
            что они не помещаются на один сервер: да, такое вполне возможно
        `,
        name: 'analyze_huge_data',
    },
    {
        text: `Нужно анализировать огромные данные: требование, которые предъявляют аналитические системы'`,
        name: 'analyze_big_data',
    },
    {
        text: `
                Повышенные требования к разграничению доступов:
                в некоторых системах доставка данных не тому пользователю критична,
                и им нужно разделение доступов, чтобы такая ситуация стала невозможной даже теоретически.
        `,
        name: 'high_access_differentiation',
    },
    {
        text: `
            Нельзя терять данные: потеря данных может быть критична. Нужно уточнять, 
            так как бывают сценарии использования базы данных, в которых такого требования нет. Например, кэш.
        `,
        name: 'cant_lose_data',
    },
    {
        text: `Данные всегда должны быть корректны: даже временная несогласованность данных критична`,
        name: 'data_must_always_be_correct',
    },
]

const db_text = document.querySelector('#databases_text')
const form = document.querySelector('#form')


function start() {
    for (let i=0; i < requirements.length; i++) {
        let requirement = requirements[i]
        let requirement_html = `
            <p>
                ${requirement.text}
            </p>
                
            <div class="form_toggle">
                <input class="hidden-requirement" type="hidden" name="${requirement.name}">
                <div class="form_toggle-item item-1">
                    <input name="radio-${i}" id="form-radio-1-${i}" type="radio" value="off" checked> 
                    <label for="form-radio-1-${i}">OFF</label>
                </div>
                <div class="form_toggle-item item-2">
                    <input name="radio-${i}" id="form-radio-2-${i}" type="radio" value="on">
                    <label for="form-radio-2-${i}">ON</label>
                </div>
            </div>
        `
        form.insertAdjacentHTML('beforeend', requirement_html)
    }
    form.insertAdjacentHTML('beforeend', '<input class="submit-form" type="submit">')
}

start()


function render_db_texts(db_data_list) {
    db_text.innerHTML = ''
    for (let db_data of db_data_list) {
        let characteristics_html = '<ul class="db-characteristics">'
        for (let characteristic of db_data.characteristics) {
            characteristics_html += `
                <li class="db-single-characteristic">
                    ${characteristic}
                </li>
            `
        }
        characteristics_html += '</ul>'
        let db_data_html = `
        <ul class="db-list">
            <li class="db-elem">
                <h3 class="db-name">
                    ${db_data.name}
                </h3>
                <p class="db-popularity">
                    Рейтинг популярности: ${db_data.popularity}
                </p>
                <p class="db-text">
                ${db_data.description}
                </p>
                ${characteristics_html}
            </li>
        </ul>
        `
        db_text.insertAdjacentHTML('beforeend', db_data_html)
    }
}


async function send_response(event) {
    event.preventDefault();

    let radio_parts = form.querySelectorAll('.form_toggle')
    let requirements = []
    for (let radio_part of radio_parts) {
        if (radio_part.querySelector('.item-2 input').checked) {
            requirements.push(radio_part.querySelector('.hidden-requirement').name + '=true')
        } 
    }

    get_parameteres = requirements.join('&')

    await fetch('/choice-db/?' + get_parameteres).then(result => {
            result.json().then(result => {render_db_texts(result)})
        },
        error => {
            alert('Что-то пошло не так. Пожалуйста, перезапустите сервер и попробуйте снова.')
      });
}

form.addEventListener('submit', send_response)
