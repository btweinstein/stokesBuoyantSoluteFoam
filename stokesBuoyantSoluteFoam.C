/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 2011-2016 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Application
    simpleFoam

Description
    Steady-state solver for incompressible, turbulent flow, using the SIMPLE
    algorithm.

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "simpleControl.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    #include "postProcess.H"

    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"
    #include "createControl.H"
    #include "createFields.H"
    #include "initContinuityErrs.H"

    while (simple.loop())
    {
        Info<< "Time = " << runTime.timeName() << nl << endl;
        
	// Now that the c-field is initialized, calculate the corresponding
	// v-field.
	
	surfaceVectorField source // Calculate the source due to devaitions from hydrostatics. 
	(
	    "source",
	    -ghf * Ra * fvc::snGrad(c)
	);
	
	double U_res_init = 1;
	double P_res_init = 1;
	
	int nStokesIter = 0;
	while((U_res_init > U_converged) || (P_res_init > p_converged))
	{
	    nStokesIter++;
	    // --- Pressure-velocity SIMPLE corrector
	    {
		#include "UEqn.H"
		#include "pEqn.H"
	    }
	}
	
	Info<< "Stokes solver converged in " << nStokesIter << " iterations." << nl << endl;
	
	#include "CourantNo.H"	

        while (simple.correctNonOrthogonal())
        {
            fvScalarMatrix cEqn
            (
                fvm::ddt(c)
              + fvm::div(phi, c)
              - fvm::laplacian(D_star, c)
            );

            cEqn.relax();
            cEqn.solve();
        }


        runTime.write();

        Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
            << "  ClockTime = " << runTime.elapsedClockTime() << " s"
            << nl << endl;	
    }

    Info<< "End\n" << endl;
    
    return 0;
}


// ************************************************************************* //
