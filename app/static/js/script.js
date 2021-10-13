 $(document).ready(function() {
 
    const URL = location.protocol + '//' + document.domain + ':' + location.port
    const date = new Date()

    const chartCanvas = document.getElementById('canvas')
    const total_income = document.getElementById('total_income')
    const total_outcome = document.getElementById('total_outcome')
    const avg_income = document.getElementById('avg_income')
    const avg_outcome = document.getElementById('avg_outcome')
    

    var default_month = date.getMonth() + 1 ;

    socket = io.connect(URL)
    socket.on('connect', function(){
        console.log('socket connected')
    })

        
    let dataChart = {
        labels:[],
        datasets:[{
            label:'income',
            fill:false, 
            data:[],
            borderColor: 'rgb(75, 192, 192)',
            tension:0.1
        },
        {
            label:'outcome',
            fill:false,
            data:[],
            borderColor:'rgb(220,20,60)', 
        }
        ]
    }
 
    var config = {
        type:'line',
        data:dataChart,
        options: {
            responsive:true

        }
    }

    const chart = new Chart(chartCanvas.getContext('2d'), config)

    function store_data(m) {
        var kons = load_data(m)
        kons.then(function(resp) {
            if(resp){
                Object.keys(resp).forEach(i => {
                    let total_inc = 0;
                    let total_out = 0;

                    total_inc += resp[i].income 
                    total_out += resp[i].outcome 

                    total_income.innerHTML = 'total income ' + total_inc 
                    total_outcome.innerHTML = 'total outcome ' + total_out 
    
                    avg_income.innerHTML = 'average income ' + parseInt(total_inc / resp[i].inc_data)
                    avg_outcome.innerHTML = 'average outcome ' + parseInt(total_out / resp[i].out_data)
                })
            }else{
                alert('no data for shown');
            }
        })
    }

                                                                              
    async function load_data(month){
        var endpoint_uri = './api/getData?month=' + month 
        let response = await fetch(endpoint_uri)
        let json_response = await response.json()
        let json_keys = await Object.keys(json_response)
        let resp_length = await json_keys.length

        if(resp_length == 0 ){
            return false
        }

        for(let i in json_keys){
            dataChart.labels[i] = json_keys[i]
            dataChart.datasets[0].data[i] = json_response[json_keys[i]].income
            dataChart.datasets[1].data[i] = json_response[json_keys[i]].outcome
            chart.update()
        }
        return json_response

    }


    $('#addincome').on('click', function(){
        var incomeval = $('#income')
        incval = parseInt(incomeval.val())
        socket.emit('send_data', {'type':'income','data':incval});
        incomeval.val('')
        
    })

    $('#addoutcome').on('click', function(){
        var outcome = $('#outcome')
        outcomeval = parseInt(outcome.val())
        socket.emit('send_data', {'type':'outcome','data':outcomeval});
        outcome.val('')

    })
    $('#showb').on('click', function(){
        var shown = parseInt($('#shown').val())
        if(isNaN(shown)){
            alert('please enter the valid number of month')
        }else{
            console.log(shown)
            store_data(shown)
        }

    })
    socket.on('message', function(data){
        alert(data);
        store_data(default_month)
    })
    store_data(default_month)

    

   
    
})
 