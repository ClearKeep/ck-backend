const OrbitDB = require('orbit-db')
const Ctl = require('ipfsd-ctl')
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

var PROTO_PATH = __dirname + '/find_user_by_email.proto';
var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true
    });
var find_user_by_email = grpc.loadPackageDefinition(packageDefinition).find_user_by_email;

var db

function pushEmailHash(call, callback) {
    console.log("pushEmailHash")
    console.log("received/email_hash:" + call.request.email_hash)

    var server_list = db.get(call.request.email_hash)
    console.log('server_list')
    console.log(server_list)

    if (server_list == undefined) {
        server_list = new Set()
    } else {
        server_list = new Set(server_list)
    }

    server_list.add(
        call.request.server
    )
    server_list = [...server_list]
    const ret = db.put(
        call.request.email_hash,
        server_list
    ).then(() => print_db_all(db))

    callback(null, {status: 'Email hash:' + call.request.email_hash});
}

function getUserFromEmailHash(call, callback) {
    console.log("getUserFromEmaiHash")
    console.log("received/email_hash:" + call.request.email_hash)
    var server_list = db.get(call.request.email_hash)
    var new_server_list = []

    if (server_list != undefined) {
        server_list.forEach(server_address => {
                new_server_list.push({address: server_address})
            }
        )
    }
    callback(null, {server_list: new_server_list});
}



const startIpfs = async (external_ip_address_for_announce) => {
    const goIpfs = {
        'go-ipfs': {
            type: 'go',
            // test: true,
            // disposable: true,
            args: ['--enable-pubsub-experiment'],
            ipfsHttpModule: require('ipfs-http-client'),
            ipfsBin: require('go-ipfs').path()
        }
    }

    var p2p_exposing_port = `12016`
    var config = {}
    config.daemon1 = {
        EXPERIMENTAL: {
            pubsub: true
        },
        config: {
            Addresses: {
                API: `/ip4/127.0.0.1/tcp/15002`,
                Swarm: [`/ip4/0.0.0.0/tcp/${p2p_exposing_port}`],
                Gateway: `/ip4/0.0.0.0/tcp/19090`,
                Announce: [
                    `/ip4/${external_ip_address_for_announce}/tcp/${p2p_exposing_port}`
                ]

            },
            Discovery: {
                MDNS: {
                    Enabled: true,
                    Interval: 0
                },
                webRTCStar: {
                    Enabled: false
                }
            }
        }
    }

    const controllerConfig = goIpfs['go-ipfs']
    controllerConfig.ipfsOptions = config.daemon1

    const ipfsd = Ctl.createController(controllerConfig)
    return ipfsd
}

function print_db_all(db) {
    console.log('----------------------------------------------------')
    console.log('----------------------------------------------------')
    console.log('----------------------------------------------------')
    for (const [key, value] of Object.entries(db.all)) {
        console.log(`${key}:${value}`)
    }
    console.log('----------------------------------------------------')
    console.log('----------------------------------------------------')
    console.log('----------------------------------------------------')
}

async function main() {

    if (process.argv[2] === undefined || process.argv[3] === undefined) {
        console.log('ERROR! Missing args')
        return -1
    }

    const external_ip_address_for_announce = process.argv[2]

    // Create DB
    // db = await orbitdb.keyvalue(
    //     'my_keyvalue_db_6',
    //     {accessController: {write: ['*']}}
    // )
    // console.log('DB address:' + db.address.toString())
    // const db_address = '/orbitdb/zdpuAppidkqvGE51yEEmrJZiCGVZi45FEieuXFhoHZTAqgycg/my_keyvalue_db_6'
    const db_address = process.argv[3]

    const ipfsd = await startIpfs(external_ip_address_for_announce)
    const ipfs = ipfsd.api
    const id = await ipfsd.api.id()
    console.log(id)

    bootstrapData = await ipfsd.api.config.get('Bootstrap')
    console.log(bootstrapData)

    const configApi = await ipfsd.api.config
    console.log(configApi)

    const orbitdb = await OrbitDB.createInstance(
        ipfs,
        {directory: `./orbitdb_directory`}
    )


    db = await orbitdb.keyvalue(db_address)
    db.events.on('replicated', (address) => {
        console.log('------------------REPLICATED------------------------')
        print_db_all(db)
    })

    console.log("Started")
    var server = new grpc.Server();
    server.addService(find_user_by_email.FindUserByEmailService.service, {
        push_email_hash: pushEmailHash,
        get_server_from_email_hash: getUserFromEmailHash
    });
    server.bindAsync(`0.0.0.0:10051`, grpc.ServerCredentials.createInsecure(), () => {
        server.start();
    });
}

main()
