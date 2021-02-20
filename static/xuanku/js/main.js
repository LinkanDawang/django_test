var COLORS = [ '0x694D8B', '0xd83784', '0xd62b2e', '0xe5de3a', '0x74b74a', '0x15a1c5' ];

var renderer;
var stage;
var vizGroup;

function init(){
	renderer = new PIXI.autoDetectRenderer(800, 600, {
		transparent: false,
		antialias: true,
		backgroundColor: 0xf6f6f6
	});
	/*
	renderer.backgroundColor = 0xf6f6f6;
	renderer.transparent = false;
	renderer.antialias = true;
	*/
	$("#visualizer").append(renderer.view);

		
	stage = new PIXI.Container();
	vizGroup = new PIXI.Container();
	stage.addChild(vizGroup);
	
	initBeast();

	$( window ).resize(onResize);
	onResize();

	requestAnimationFrame(animate);
}

function animate() {
	renderer.render(stage);
	requestAnimationFrame( animate );
	
	if(isHomepageActive) {
		drawCurves();
		noiseTime += 0.002;
	}
	
	drawBeast();
}

function onResize(){
	renderer.resize(window.innerWidth,window.innerHeight);
	vizGroup.x = renderer.width/2;
	vizGroup.y = renderer.height/2;

	resizeBeast();
	
	if(isHomepageActive) {
		resizeHomepage();
	}
}

$(function(){
	init();
}); 
