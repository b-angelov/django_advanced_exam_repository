const mainUrl = window.location.protocol + "//" + window.location.host + '/orth_calendar'

const urls = {
    'saints': {
        'url':mainUrl +'/saints',
        'single':'/%single', /* objecs id  in database*/
        'related_holidays': 'related_holidays=%related_holidays', /* bool, 1 or 0 */
        'related_feasts': 'related_feasts=%related_feasts', /* bool, 1 or 0 */
        undefined:'',

    },
    'feasts': {
        'url':mainUrl +'/feasts',
        'single': '/%single', /* objecs id  in database*/
        'related_holidays': 'related_holidays=%related_holidays', /* bool, 1 or 0 */
        'related_feasts': 'related_saints=%related_saints', /* bool, 1 or 0 */
        undefined:'',

    },
    'holidays':{
        'url':mainUrl +'/holidays',
        'single': '/%single', /* objecs id  in database*/
        'by_date': '/%by_date/', /* date in format yyyy-mm-dd*/
        'by_month': '/by_month/%by_month/', /* month number */
        'related': 'related=%related', /* bool, 1 or 0 */
        'calendar': 'calendar=%calendar', /* could be J G or JIG*/
        'year': 'year=%year', /* year number */
        undefined:'',
    }
}

function urlJoiner(point_name, params={}){
    const obj = {...urls[point_name]}
    let url = obj['url'] || ''
    url += params['single'] ? obj['single'] || '' : ''
    if (!params['single']){
        url += params['by_date'] ? obj['by_date'] || '' : ''
    }
    url += params['by_month'] ? obj['by_month'] || '' : ''
    const pattern = /%[^\?\/\&]+/g
    url = url.replace(pattern, elem=> {
        return params[elem.replace('%','')] || ''
    })
    url += '?'
    obj['single'] = null
    obj['by_date'] = null
    obj['by_month'] = null
    let parts = []
    for (const param of Object.keys(params)){
        obj[param] ? parts.push(obj[param]) : '';
    }
    url += parts.join('&').replace(pattern, elem=>params[elem.replace('%','')]||'')
    return url

}

async function fetchUrl(url, method, params){
    let response = await fetch(url,{
        method:method.toUpperCase(),
        headers: {...params.headers},
        body: JSON.stringify(params.body)
    })
    response = await response.json()
    return response
}


async function getFromUrl(point_name, url_params={}){
    const url = urlJoiner(point_name,url_params)
    return await fetchUrl(url,'get')
}

async function modifyUrl(point_name, method, url_params={}, method_params={}){
    const url = urlJoiner(point_name,url_params)
    return await fetchUrl(url,method,method_params)
}

const getUrl = (point_name,url_params={},method_params={}) => modifyUrl(point_name,'get', url_params, method_params);
const postUrl = (point_name,url_params={},method_params={}) => modifyUrl(point_name,'patch', url_params, method_params);
const patchUrl = (point_name,url_params={},method_params={}) => modifyUrl(point_name,'post', url_params, method_params);
const putUrl = (point_name,url_params={},method_params={}) => modifyUrl(point_name,'put', url_params, method_params);
const deleteUrl = (point_name,url_params={},method_params={}) => modifyUrl(point_name,'delete', url_params, method_params);


export {postUrl as post,patchUrl as patch,putUrl as put,deleteUrl as del,getUrl as get};