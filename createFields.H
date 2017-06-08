Info<< "Reading field p\n" << endl;
volScalarField p
(
    IOobject
    (
        "p",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading field U\n" << endl;
volVectorField U
(
    IOobject
    (
        "U",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading field c\n" << endl;
volScalarField c
(
    IOobject
    (
        "c",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);


#include "createPhi.H"


label pRefCell = 0;
scalar pRefValue = 0.0;
setRefCell(p, simple.dict(), pRefCell, pRefValue);
mesh.setFluxRequired(p.name());

// Lookup parameters is transport properties

Info<< "Reading Transport Properties... \n" << endl;
IOdictionary transportProperties
(
     IOobject
     (
        "transportProperties",
        runTime.constant(),
        mesh,
        IOobject::MUST_READ_IF_MODIFIED,
        IOobject::NO_WRITE
     )
);

// Set nu_star and D_star...only one input parameter, Ra. 
dimensionedScalar nu_star
(
	"nu_star",
	dimensionSet(0, 2, -1, 0, 0, 0, 0),
	1.0
);

dimensionedScalar D_star
(
	"D_star",
	dimensionSet(0, 2, -1, 0, 0, 0, 0),
	1.0
);


Info<< "Reading Ra \n" << endl; //Units of (L^4/T^2)*(1/Quantity)
dimensionedScalar Ra
(
     transportProperties.lookup("Ra")
 );

// Create the gravitational unit vector...presumably in the zhat direction
// So be careful when defining your coordinate system 
// (especially in 2d, make it x-z, not x-y). 
vector ghat (0.0,0.0,-1.0);
